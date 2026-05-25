import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth import get_current_user
from src.database import get_session
from src.models.projeto_db import Blueprint, Project, Report
from src.modules.drill import processar_dxf
from src.modules.Memorial.generatorteste import run_integration

router = APIRouter(prefix="/processamento", tags=["processamento"])
memorial_router = APIRouter(prefix="/memorial_calculo", tags=["memorial_calculo"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOADS_DIR = BACKEND_ROOT / "uploads"
TEMPLATE_FILE = BACKEND_ROOT / "src" / "templates" / "memorial_model.xlsx"


def _get_project(db: Session, project_id: int) -> Project:
    project = db.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto nao encontrado.",
        )
    return project


def _resolve_upload_path(relative_path: str | None) -> Path | None:
    if not relative_path:
        return None

    safe_path = Path(relative_path)
    if safe_path.is_absolute() or ".." in safe_path.parts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Caminho de planta invalido.",
        )

    uploads_root = UPLOADS_DIR.resolve()
    file_path = (uploads_root / safe_path).resolve()

    try:
        file_path.relative_to(uploads_root)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Caminho de planta fora da pasta de uploads.",
        ) from exc

    return file_path


def _get_project_dxf_files(db: Session, project_id: int) -> list[Path]:
    blueprints = db.execute(
        select(Blueprint).where(Blueprint.id_project == project_id)
    ).scalars().all()

    dxf_files: list[Path] = []
    for blueprint in blueprints:
        file_path = _resolve_upload_path(blueprint.path)
        if file_path and file_path.suffix.lower() == ".dxf":
            dxf_files.append(file_path)

    existing_files = [file_path for file_path in dxf_files if file_path.exists()]
    if not existing_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum arquivo DXF encontrado para este projeto.",
        )

    return existing_files


def _latest_report(db: Session, project_id: int) -> Report | None:
    return db.execute(
        select(Report)
        .where(Report.id_project == project_id)
        .order_by(Report.id.desc())
    ).scalars().first()


def _save_report_path(db: Session, project_id: int, relative_path: str) -> Report:
    report = _latest_report(db, project_id)

    if report:
        report.path = relative_path
    else:
        report = Report(path=relative_path, id_project=project_id)
        db.add(report)

    db.commit()
    db.refresh(report)
    return report


def _extract_drill_data(dxf_file: Path) -> dict[str, Any]:
    extracted_data = processar_dxf(str(dxf_file))

    if not isinstance(extracted_data, dict):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="O drill.py retornou um formato invalido.",
        )

    if extracted_data.get("erro"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Falha ao extrair dados do DXF com drill.py: {extracted_data['erro']}",
        )

    return extracted_data


def _save_drill_json(project_id: int, generated_dir: Path, extracted_data: dict[str, Any]) -> str:
    output_file = generated_dir / f"projeto_{project_id}_drill.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=2)

    return f"{project_id}/generated/{output_file.name}"


def _get_drill_json_path(report: Report) -> Path | None:
    report_path = _resolve_upload_path(report.path)
    if not report_path:
        return None

    drill_path = report_path.with_name(report_path.name.replace("_memorial_calculo.xlsx", "_drill.json"))
    return drill_path if drill_path.exists() else None


def _load_drill_data(report: Report) -> dict[str, Any] | None:
    drill_path = _get_drill_json_path(report)

    if not drill_path:
        return None

    try:
        with drill_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return None


def _build_result_summary(project: Project, report: Report, extracted_data: dict[str, Any] | None) -> dict[str, Any]:
    resumo_global = extracted_data.get("resumo_global", {}) if extracted_data else {}

    return {
        "resumo_executivo": {
            "Projeto": project.name,
            "Memorial de calculo": "Arquivo gerado a partir dos dados extraidos pelo drill.py.",
            "Arquivo": Path(report.path).name,
            "Portas": resumo_global.get("quantidade_total_portas", 0),
            "Janelas": resumo_global.get("quantidade_total_janelas", 0),
            "Volume liquido de alvenaria (m3)": resumo_global.get("volume_final_liquido_alvenaria_m3", 0),
            "Volume total de vigas (m3)": resumo_global.get("volume_total_vigas_m3", 0),
            "Volume total de colunas (m3)": resumo_global.get("volume_total_colunas_m3", 0),
            "Area total de laje (m2)": resumo_global.get("area_total_laje_m2", 0),
            "Comprimento total de fios (m)": resumo_global.get("comprimento_total_fios_m", 0),
            "Comprimento total de canos (m)": resumo_global.get("comprimento_total_canos_m", 0),
        },
        "dados_extraidos_drill": extracted_data or {},
    }


def _report_to_payload(
    request: Request,
    report: Report,
    project: Project,
    extracted_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if extracted_data is None:
        extracted_data = _load_drill_data(report)

    drill_path = _get_drill_json_path(report)

    return {
        "tipo": "memorial_calculo",
        "file_url": str(
            request.url_for("download_memorial_calculo", project_id=project.id)
        ),
        "path": report.path,
        "extraction_path": str(drill_path.relative_to(UPLOADS_DIR)) if drill_path else None,
        "resultado": json.dumps(_build_result_summary(project, report, extracted_data), ensure_ascii=False),
    }


def _generate_memorial(db: Session, project_id: int, request: Request) -> dict[str, Any]:
    project = _get_project(db, project_id)
    dxf_files = _get_project_dxf_files(db, project_id)

    project_dir = UPLOADS_DIR / str(project_id)
    generated_dir = project_dir / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    output_file = generated_dir / f"projeto_{project_id}_memorial_calculo.xlsx"
    relative_output = f"{project_id}/generated/{output_file.name}"
    extracted_data = _extract_drill_data(dxf_files[0])
    _save_drill_json(project_id, generated_dir, extracted_data)

    try:
        run_integration(
            dxf_file=str(dxf_files[0]),
            template_file=str(TEMPLATE_FILE),
            output_file=str(output_file),
            quantitativos_dxf=extracted_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    report = _save_report_path(db, project_id, relative_output)
    return _report_to_payload(request, report, project, extracted_data)


@router.post("/{project_id}", summary="Processar projeto")
async def process_project(
    project_id: int,
    request: Request,
    stream: bool = False,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_session),
):
    if not stream:
        return [_generate_memorial(db, project_id, request)]

    def event_stream():
        yield "data: Iniciando processamento do projeto...\n\n"
        try:
            result = _generate_memorial(db, project_id, request)
            yield "data: Memorial de calculo gerado com sucesso.\n\n"
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except HTTPException as exc:
            yield f"data: ERRO: {exc.detail}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            db.rollback()
            yield f"data: ERRO: Falha ao processar projeto: {exc}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/{project_id}/resultado", summary="Buscar resultado do processamento")
async def get_processing_result(
    project_id: int,
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_session),
):
    project = _get_project(db, project_id)
    report = _latest_report(db, project_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado de processamento nao encontrado.",
        )

    return [_report_to_payload(request, report, project)]


@memorial_router.get(
    "/projeto/{project_id}/download",
    name="download_memorial_calculo",
    summary="Baixar memorial de calculo",
)
async def download_memorial_calculo(
    project_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_session),
):
    _get_project(db, project_id)
    report = _latest_report(db, project_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memorial de calculo nao encontrado.",
        )

    file_path = _resolve_upload_path(report.path)
    if not file_path or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo do memorial nao encontrado.",
        )

    return FileResponse(
        path=file_path,
        filename=f"projeto_{project_id}_memorial_calculo.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
