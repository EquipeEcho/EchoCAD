import asyncio
import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_user
from src.controller.crud_users import get_user_groq_api_key
from src.database import get_async_session
from src.models.projeto_db import Blueprint, Project, Report, Specification
from src.modules.EspecificacoesTecnicas import gerar_especificacoes
from src.modules.drill import processar_dxf
from src.modules.Memorial.generatorteste import run_integration

router = APIRouter(prefix="/processamento", tags=["processamento"])
memorial_router = APIRouter(prefix="/memorial_calculo", tags=["memorial_calculo"])
technical_spec_router = APIRouter(
    prefix="/especificacoes_tecnicas", tags=["especificacoes_tecnicas"]
)

BACKEND_ROOT = Path(__file__).resolve().parents[2]
UPLOADS_DIR = BACKEND_ROOT / "uploads"
TEMPLATE_FILE = BACKEND_ROOT / "src" / "templates" / "memorial_model.xlsx"


async def _get_project(db: AsyncSession, project_id: int) -> Project:
    project = (
        await db.execute(select(Project).where(Project.id == project_id))
    ).scalar_one_or_none()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto nao encontrado.",
        )
    return project


def _resolve_upload_path(relative_path: str | None) -> Path | None:
    if not relative_path:
        return None

    safe_path = Path(relative_path.replace("\\", "/"))
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


async def _get_project_dxf_files(db: AsyncSession, project_id: int) -> list[Path]:
    blueprints = (
        (await db.execute(select(Blueprint).where(Blueprint.id_project == project_id)))
        .scalars()
        .all()
    )

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


async def _latest_report(db: AsyncSession, project_id: int) -> Report | None:
    return (
        (
            await db.execute(
                select(Report)
                .where(Report.id_project == project_id)
                .order_by(Report.id.desc())
            )
        )
        .scalars()
        .first()
    )


async def _latest_specification(
    db: AsyncSession, project_id: int
) -> Specification | None:
    return (
        (
            await db.execute(
                select(Specification)
                .where(Specification.id_project == project_id)
                .order_by(Specification.id.desc())
            )
        )
        .scalars()
        .first()
    )


async def _save_report_path(
    db: AsyncSession, project_id: int, relative_path: str
) -> Report:
    report = await _latest_report(db, project_id)

    if report:
        report.path = relative_path
    else:
        report = Report(path=relative_path, id_project=project_id)
        db.add(report)

    await db.commit()
    await db.refresh(report)
    return report


async def _save_specification_path(
    db: AsyncSession, project_id: int, relative_path: str
) -> Specification:
    specification = await _latest_specification(db, project_id)

    if specification:
        specification.path = relative_path
    else:
        specification = Specification(path=relative_path, id_project=project_id)
        db.add(specification)

    await db.commit()
    await db.refresh(specification)
    return specification


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


def _save_drill_json(
    project_id: int, generated_dir: Path, extracted_data: dict[str, Any]
) -> str:
    output_file = generated_dir / f"projeto_{project_id}_drill.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=2)

    return f"{project_id}/generated/{output_file.name}"


def _get_drill_json_path(report: Report) -> Path | None:
    report_path = _resolve_upload_path(report.path)
    if not report_path:
        return None

    drill_path = report_path.with_name(
        report_path.name.replace("_memorial_calculo.xlsx", "_drill.json")
    )
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


def _specification_relative_path(project_id: int) -> str:
    return f"{project_id}/generated/projeto_{project_id}_especificacoes_tecnicas.docx"


def _specification_output_path(project_id: int) -> Path:
    return UPLOADS_DIR / _specification_relative_path(project_id)


async def _get_specification_path(db: AsyncSession, project_id: int) -> Path | None:
    specification = await _latest_specification(db, project_id)

    if specification:
        specification_path = _resolve_upload_path(specification.path)
        if specification_path and specification_path.exists():
            return specification_path

    fallback_path = _specification_output_path(project_id)
    return fallback_path if fallback_path.exists() else None


def _build_result_summary(
    project: Project,
    report: Report,
    extracted_data: dict[str, Any] | None,
    specification_path: Path | None = None,
    specification_error: str | None = None,
) -> dict[str, Any]:
    resumo_global = extracted_data.get("resumo_global", {}) if extracted_data else {}

    return {
        "resumo_executivo": {
            "Projeto": project.name,
            "Memorial de calculo": "Arquivo gerado a partir dos dados extraidos pelo drill.py.",
            "Arquivo": Path(report.path).name,
            "Especificacoes tecnicas": (
                specification_path.name
                if specification_path
                else "Nao geradas"
                if specification_error
                else "Indisponivel"
            ),
            "Portas": resumo_global.get("quantidade_total_portas", 0),
            "Janelas": resumo_global.get("quantidade_total_janelas", 0),
            "Volume liquido de alvenaria (m3)": resumo_global.get(
                "volume_final_liquido_alvenaria_m3", 0
            ),
            "Volume total de vigas (m3)": resumo_global.get("volume_total_vigas_m3", 0),
            "Volume total de colunas (m3)": resumo_global.get(
                "volume_total_colunas_m3", 0
            ),
            "Area total de laje (m2)": resumo_global.get("area_total_laje_m2", 0),
            "Comprimento total de fios (m)": resumo_global.get(
                "comprimento_total_fios_m", 0
            ),
            "Comprimento total de canos (m)": resumo_global.get(
                "comprimento_total_canos_m", 0
            ),
        },
        "erro_especificacoes_tecnicas": specification_error,
        "dados_extraidos_drill": extracted_data or {},
    }


def _report_to_payload(
    request: Request,
    report: Report,
    project: Project,
    extracted_data: dict[str, Any] | None = None,
    specification_path: Path | None = None,
    specification_error: str | None = None,
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
        "extraction_path": drill_path.relative_to(UPLOADS_DIR).as_posix()
        if drill_path
        else None,
        "resultado": json.dumps(
            _build_result_summary(
                project,
                report,
                extracted_data,
                specification_path=specification_path,
                specification_error=specification_error,
            ),
            ensure_ascii=False,
        ),
    }


def _specification_to_payload(
    request: Request,
    project: Project,
    specification_path: Path,
) -> dict[str, Any]:
    relative_path = specification_path.relative_to(UPLOADS_DIR).as_posix()
    return {
        "tipo": "especificacoes_tecnicas",
        "file_url": str(
            request.url_for("download_especificacoes_tecnicas", project_id=project.id)
        ),
        "path": relative_path,
        "resultado": json.dumps(
            {
                "resumo_executivo": {
                    "Projeto": project.name,
                    "Especificacoes tecnicas": specification_path.name,
                    "Arquivo": specification_path.name,
                }
            },
            ensure_ascii=False,
        ),
    }


async def _generate_specification(
    db: AsyncSession,
    project: Project,
    dxf_file: Path,
    generated_dir: Path,
    extracted_data: dict[str, Any] | None = None,
    api_key: str | None = None,
) -> Path:
    output_file = generated_dir / f"projeto_{project.id}_especificacoes_tecnicas.docx"

    arquivo_gerado = await gerar_especificacoes(
        dxf_file=str(dxf_file),
        output_path=str(output_file),
        nome_projeto=project.name,
        api_key=api_key,
        drill_data=extracted_data,
    )

    relative_output = arquivo_gerado.relative_to(UPLOADS_DIR).as_posix()
    try:
        await _save_specification_path(db, project.id, relative_output)
    except Exception:
        await db.rollback()
    return arquivo_gerado


async def _generate_project_documents(
    db: AsyncSession, project_id: int, request: Request, groq_api_key: str | None = None
) -> list[dict[str, Any]]:
    project = await _get_project(db, project_id)
    dxf_files = await _get_project_dxf_files(db, project_id)

    project_dir = UPLOADS_DIR / str(project_id)
    generated_dir = project_dir / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    dxf_file = dxf_files[0]
    output_file = generated_dir / f"projeto_{project_id}_memorial_calculo.xlsx"
    relative_output = f"{project_id}/generated/{output_file.name}"
    extracted_data = _extract_drill_data(dxf_file)
    _save_drill_json(project_id, generated_dir, extracted_data)

    try:
        run_integration(
            dxf_file=str(dxf_file),
            template_file=str(TEMPLATE_FILE),
            output_file=str(output_file),
            quantitativos_dxf=extracted_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    specification_path: Path | None = None
    specification_error: str | None = None
    try:
        specification_path = await _generate_specification(
            db,
            project,
            dxf_file,
            generated_dir,
            extracted_data=extracted_data,
            api_key=groq_api_key,
        )
    except Exception as exc:
        await db.rollback()
        specification_error = str(exc)

    report = await _save_report_path(db, project_id, relative_output)
    payloads = [
        _report_to_payload(
            request,
            report,
            project,
            extracted_data,
            specification_path=specification_path,
            specification_error=specification_error,
        )
    ]

    if specification_path and specification_path.exists():
        payloads.append(_specification_to_payload(request, project, specification_path))

    return payloads


@router.post("/{project_id}", summary="Processar projeto")
async def process_project(
    project_id: int,
    request: Request,
    stream: bool = False,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    groq_api_key = get_user_groq_api_key(current_user)
    if not stream:
        return await _generate_project_documents(db, project_id, request, groq_api_key)

    async def event_stream():
        yield "data: Iniciando processamento do projeto...\n\n"
        task = asyncio.create_task(
            _generate_project_documents(db, project_id, request, groq_api_key)
        )
        elapsed = 0
        try:
            while not task.done():
                await asyncio.sleep(12)
                elapsed += 12
                yield (
                    "data: Gerando especificacoes tecnicas com IA. "
                    f"Ainda trabalhando... {elapsed}s\n\n"
                )

            result = await task
            yield "data: Memorial de calculo gerado com sucesso.\n\n"
            if any(item.get("tipo") == "especificacoes_tecnicas" for item in result):
                yield "data: Especificacoes tecnicas geradas com sucesso.\n\n"
            else:
                yield (
                    "data: Memorial gerado. As especificacoes tecnicas nao foram "
                    "concluidas pela IA neste processamento.\n\n"
                )
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"
        except HTTPException as exc:
            if not task.done():
                task.cancel()
            yield f"data: ERRO: {exc.detail}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as exc:
            if not task.done():
                task.cancel()
            await db.rollback()
            yield f"data: ERRO: Falha ao processar projeto: {exc}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/{project_id}/resultado", summary="Buscar resultado do processamento")
async def get_processing_result(
    project_id: int,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    project = await _get_project(db, project_id)
    report = await _latest_report(db, project_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado de processamento nao encontrado.",
        )

    specification_path = await _get_specification_path(db, project_id)
    payloads = [
        _report_to_payload(
            request, report, project, specification_path=specification_path
        )
    ]
    if specification_path:
        payloads.append(_specification_to_payload(request, project, specification_path))

    return payloads


@memorial_router.get(
    "/projeto/{project_id}/download",
    name="download_memorial_calculo",
    summary="Baixar memorial de calculo",
)
async def download_memorial_calculo(
    project_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    project = await _get_project(db, project_id)
    report = await _latest_report(db, project_id)

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


@technical_spec_router.get(
    "/projeto/{project_id}/download",
    name="download_especificacoes_tecnicas",
    summary="Baixar especificacoes tecnicas",
)
async def download_especificacoes_tecnicas(
    project_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    project = await _get_project(db, project_id)
    file_path = await _get_specification_path(db, project_id)

    if not file_path or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo de especificacoes tecnicas nao encontrado.",
        )

    return FileResponse(
        path=file_path,
        filename=f"projeto_{project_id}_especificacoes_tecnicas.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
