import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import {
  CheckCircleIcon,
  DownloadIcon,
  FileTypeIcon,
  InfoCircleIcon,
  SpinnerIcon,
} from "../components/Icons";
import { ProjectSaveModal } from "../components/ProjectSaveModal";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../hooks/usePrototype";
import { API_BASE_URL } from "../services/api";
import { FileKind, ProjectSaveInput } from "../types/documents";

type ResultDownloadAsset = {
  id: string;
  title: string;
  description: string;
  fileHint: string;
  fileName: string;
  kind: FileKind;
  url?: string;
  status: "ready" | "pending" | "unavailable";
  statusLabel: string;
  meta: string;
};

type ResultRouteState = {
  refresh?: boolean;
  projectId?: number;
};

function getTableValue(rows: { label: string; value: string }[], label: string) {
  return rows.find((row) => row.label === label)?.value;
}

function toNumber(value: string | undefined) {
  if (!value) {
    return 0;
  }

  const parsed = Number(value.replace(",", "."));
  return Number.isFinite(parsed) ? parsed : 0;
}

function hasGeneratedSpec(value: string | undefined) {
  if (!value) {
    return false;
  }

  const normalized = value.toLowerCase();
  return !normalized.includes("nao gerad") && !normalized.includes("indisponivel");
}

export function ResultPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const {
    currentDocument,
    downloadDocumentAsset,
    saveCurrentProject,
    shouldPromptProjectSave,
    startAIProcessing,
    isAIProcessing,
    refreshCurrentDocument,
    activeProjectData,
  } = usePrototype();
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [downloadingAssetId, setDownloadingAssetId] = useState<string | null>(null);
  const refreshedIds = useRef<Set<number>>(new Set());

  const routeState = location.state as ResultRouteState | null;

  const resolvedProjectId = useMemo(() => {
    if (routeState?.projectId) {
      return routeState.projectId;
    }

    if (activeProjectData?.projectId) {
      return activeProjectData.projectId;
    }

    const parsedId = Number(currentDocument?.id);
    return Number.isFinite(parsedId) ? parsedId : undefined;
  }, [activeProjectData?.projectId, currentDocument?.id, routeState?.projectId]);

  const isPending =
    !currentDocument ||
    (currentDocument.file_urls.length === 0 && currentDocument.tableRows.length === 0);

  const downloadAssets = useMemo<ResultDownloadAsset[]>(() => {
    const projectId = resolvedProjectId;
    const fileUrls = currentDocument?.file_urls ?? [];
    const tableRows = currentDocument?.tableRows ?? [];
    const hasMemorial = fileUrls.some((url) => url.includes("memorial_calculo"));
    const hasSpecFile =
      fileUrls.some((url) => url.includes("especificacoes_tecnicas")) ||
      hasGeneratedSpec(getTableValue(tableRows, "Especificacoes tecnicas"));
    const memorialStatus = isPending ? "pending" : hasMemorial || projectId ? "ready" : "unavailable";
    const specStatus = isPending ? "pending" : hasSpecFile ? "ready" : "unavailable";

    return [
      {
        id: "memorial-calculo",
        title: "Memorial de cálculos",
        description: "Arquivo gerado com cálculos, premissas e validações extraídas do projeto.",
        fileHint: "Arquivo do memorial de cálculos",
        fileName: projectId
          ? `projeto_${projectId}_memorial_calculo.xlsx`
          : "memorial_calculo.xlsx",
        kind: "xlsx",
        url: projectId
          ? `${API_BASE_URL}/memorial_calculo/projeto/${projectId}/download`
          : undefined,
        status: memorialStatus,
        statusLabel:
          memorialStatus === "ready"
            ? "Gerado"
            : memorialStatus === "pending"
              ? "Aguardando"
              : "Indisponível",
        meta:
          memorialStatus === "ready"
            ? "XLSX pronto para download"
            : memorialStatus === "pending"
              ? "Disponível após o processamento"
              : "Processamento ainda não gerou este arquivo",
      },
      {
        id: "especificacoes-tecnicas",
        title: "Especificações técnicas",
        description: "Documento técnico consolidado com critérios, materiais e referências normativas.",
        fileHint: "Arquivo das especificações técnicas",
        fileName: projectId
          ? `projeto_${projectId}_especificacoes_tecnicas.docx`
          : "especificacoes_tecnicas.docx",
        kind: "docx",
        url: projectId
          ? `${API_BASE_URL}/especificacoes_tecnicas/projeto/${projectId}/download`
          : undefined,
        status: specStatus,
        statusLabel:
          specStatus === "ready"
            ? "Gerado"
            : specStatus === "pending"
              ? "Aguardando"
              : "Indisponível",
        meta:
          specStatus === "ready"
            ? "DOCX gerado pela IA"
            : specStatus === "pending"
              ? "Disponível após o processamento"
              : "Não foi gerado para este processamento",
      },
    ];
  }, [currentDocument?.file_urls, currentDocument?.tableRows, isPending, resolvedProjectId]);

  const technicalChips = useMemo(() => {
    const rows = currentDocument?.tableRows ?? [];
    const chips: string[] = [];

    if (toNumber(getTableValue(rows, "Volume liquido de alvenaria (m3)")) > 0) {
      chips.push("Alvenaria");
    }
    if (
      toNumber(getTableValue(rows, "Volume total de vigas (m3)")) > 0 ||
      toNumber(getTableValue(rows, "Volume total de colunas (m3)")) > 0
    ) {
      chips.push("Estrutura");
    }
    if (toNumber(getTableValue(rows, "Area total de laje (m2)")) > 0) {
      chips.push("Laje");
    }
    if (toNumber(getTableValue(rows, "Comprimento total de fios (m)")) > 0) {
      chips.push("Elétrica");
    }
    if (toNumber(getTableValue(rows, "Comprimento total de canos (m)")) > 0) {
      chips.push("Hidráulica");
    }
    if (
      toNumber(getTableValue(rows, "Portas")) > 0 ||
      toNumber(getTableValue(rows, "Janelas")) > 0
    ) {
      chips.push("Esquadrias");
    }
    if (hasGeneratedSpec(getTableValue(rows, "Especificacoes tecnicas"))) {
      chips.push("Especificações técnicas");
    }

    return chips;
  }, [currentDocument?.tableRows]);

  const resultNotices = useMemo(() => {
    if (!currentDocument) {
      return [];
    }

    const notices: string[] = [];
    const specAsset = downloadAssets.find((asset) => asset.id === "especificacoes-tecnicas");

    if (isPending) {
      notices.push("Este projeto ainda precisa ser processado para liberar os arquivos finais.");
    }

    if (!isPending && specAsset?.status === "unavailable") {
      notices.push("As especificações técnicas não foram geradas neste processamento. O memorial continua disponível.");
    }

    if (!isPending && technicalChips.length === 0) {
      notices.push("Nenhuma disciplina técnica foi identificada no resumo extraído do projeto.");
    }

    return notices;
  }, [currentDocument, downloadAssets, isPending, technicalChips.length]);

  useEffect(() => {
    const handleInitialLoad = async () => {
      if (
        routeState?.refresh &&
        routeState.projectId &&
        !refreshedIds.current.has(routeState.projectId)
      ) {
        const projectId = routeState.projectId;
        refreshedIds.current.add(projectId);
        setIsRefreshing(true);
        await refreshCurrentDocument(projectId);
        setIsRefreshing(false);
        navigate(location.pathname, { replace: true, state: {} });
        return;
      }

      if (
        currentDocument &&
        currentDocument.file_urls.length === 0 &&
        currentDocument.tableRows.length === 0
      ) {
        const projectId = Number(currentDocument.id);

        if (Number.isFinite(projectId) && !refreshedIds.current.has(projectId)) {
          refreshedIds.current.add(projectId);
          refreshCurrentDocument(projectId);
        }
      }
    };

    handleInitialLoad();
  }, [currentDocument, location.pathname, navigate, refreshCurrentDocument, routeState]);

  useEffect(() => {
    if (currentDocument && shouldPromptProjectSave && !currentDocument.projectInfo) {
      setShowProjectForm(true);
    }
  }, [currentDocument, shouldPromptProjectSave]);

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1);
      return;
    }

    navigate("/");
  };

  const handleSaveProject = (projectInfo: ProjectSaveInput) => {
    saveCurrentProject(projectInfo);
    setShowProjectForm(false);
  };

  const handleStartProcessing = () => {
    if (!currentDocument) {
      return;
    }

    const projectId = resolvedProjectId ?? Number(currentDocument.id);

    if (!Number.isFinite(projectId)) {
      return;
    }

    const projectInfo: ProjectSaveInput = {
      name:
        currentDocument.projectInfo?.name ||
        currentDocument.title.replace(/^Memorial.*?-\s*/, ""),
      cliente: currentDocument.projectInfo?.cliente,
      descricao: currentDocument.projectInfo?.descricao || currentDocument.summary,
    };

    startAIProcessing(projectId, projectInfo, []);
    navigate("/processando");
  };

  const handleDownloadAsset = async (asset: ResultDownloadAsset) => {
    if (downloadingAssetId) {
      return;
    }

    setDownloadingAssetId(asset.id);

    try {
      await downloadDocumentAsset(asset.url, asset.fileName);
    } finally {
      setDownloadingAssetId(null);
    }
  };

  if (!currentDocument) {
    return (
      <main className="page">
        <div className="page__content page__content--narrow">
          <EmptyState
            tone="error"
            icon={<InfoCircleIcon />}
            title="Nenhum memorial disponível"
            description="Conclua um processamento ou abra um item do histórico para visualizar o resultado."
            actionLabel="Ir para Home"
            onAction={() => navigate("/")}
          />
        </div>
      </main>
    );
  }

  if (isRefreshing) {
    return (
      <main className="page">
        <div className="page__content page__content--narrow">
          <EmptyState
            icon={<SpinnerIcon className="spin" />}
            title="Carregando resultados..."
            description="Buscando as informações processadas pela IA no servidor."
          />
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <div className="page__content page__content--result">
        <section className="result-hero" aria-labelledby="result-title">
          <div
            className={`result-hero__icon${isPending ? " result-hero__icon--pending" : ""}`}
            aria-hidden="true"
          >
            {isPending ? <InfoCircleIcon /> : <CheckCircleIcon />}
          </div>
          <SectionTitle
            className="result-hero__heading"
            eyebrow="Resultado"
            titleId="result-title"
            title={
              isPending
                ? "Documentos aguardando geração"
                : "Documentos prontos para download"
            }
            description={
              isPending
                ? "Este projeto ainda precisa passar pelo processamento para liberar o memorial de cálculos e as especificações técnicas."
                : "Baixe os arquivos finais gerados para este projeto."
            }
            align="center"
          />
        </section>

        <section className="result-insights" aria-label="Resumo técnico detectado">
          <div className="result-insights__group">
            <p className="result-insights__label">Disciplinas detectadas</p>
            {technicalChips.length > 0 ? (
              <div className="result-chip-list">
                {technicalChips.map((chip) => (
                  <span key={chip} className="result-chip">
                    {chip}
                  </span>
                ))}
              </div>
            ) : (
              <p className="result-insights__empty">
                As disciplinas aparecem aqui depois que o processamento extrai dados do DXF.
              </p>
            )}
          </div>

          {resultNotices.length > 0 ? (
            <div className="result-notices" role="status" aria-live="polite">
              {resultNotices.map((notice) => (
                <p key={notice} className="result-notice">
                  {notice}
                </p>
              ))}
            </div>
          ) : null}
        </section>

        <SurfaceCard
          as="section"
          className="result-downloads"
          aria-labelledby="result-downloads-title"
        >
          <div className="result-downloads__header">
            <div>
              <p className="result-downloads__eyebrow">Arquivos gerados</p>
              <h2 id="result-downloads-title" className="result-downloads__title">
                Entregáveis técnicos
              </h2>
            </div>
            {resolvedProjectId ? (
              <span
                className="result-downloads__badge"
                aria-label={`Projeto ${resolvedProjectId}`}
              >
                <span className="result-downloads__badge-label">Projeto</span>
                <strong className="result-downloads__badge-value">
                  {resolvedProjectId}
                </strong>
              </span>
            ) : null}
          </div>

          <div className="result-downloads__grid">
            {downloadAssets.map((asset) => {
              const isDownloading = downloadingAssetId === asset.id;

              return (
                <article key={asset.id} className="result-download-card">
                  <div className="result-download-card__icon" aria-hidden="true">
                    <FileTypeIcon kind={asset.kind} />
                  </div>
                  <div className="result-download-card__body">
                    <h3 className="result-download-card__title">{asset.title}</h3>
                    <p className="result-download-card__description">
                      {asset.description}
                    </p>
                    <p className="result-download-card__meta">
                      {asset.meta}
                    </p>
                  </div>
                  <span
                    className={`result-download-card__status result-download-card__status--${asset.status}`}
                  >
                    {asset.statusLabel}
                  </span>
                  <Button
                    variant="primary"
                    leadingIcon={
                      isDownloading ? <SpinnerIcon className="spin" /> : <DownloadIcon />
                    }
                    onClick={() => handleDownloadAsset(asset)}
                    disabled={asset.status !== "ready" || isDownloading || !asset.url}
                  >
                    {isDownloading ? "Baixando..." : "Baixar"}
                  </Button>
                </article>
              );
            })}
          </div>
        </SurfaceCard>

        <div className="result-actions">
          {isPending ? (
            <Button
              variant="primary"
              onClick={handleStartProcessing}
              disabled={isAIProcessing}
            >
              {isAIProcessing ? "Processando..." : "Iniciar processamento agora"}
            </Button>
          ) : null}

          <Button variant="secondary" onClick={() => setShowProjectForm(true)}>
            {currentDocument.projectInfo ? "Editar informações" : "Salvar projeto"}
          </Button>

          <Button variant="secondary" onClick={handleBack}>
            Voltar
          </Button>
        </div>

        <ProjectSaveModal
          open={showProjectForm}
          document={currentDocument}
          onClose={() => setShowProjectForm(false)}
          onSave={handleSaveProject}
        />
      </div>
    </main>
  );
}
