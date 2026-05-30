import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import { CheckCircleIcon, InfoCircleIcon } from "../components/Icons";
import { usePrototype } from "../hooks/usePrototype";
import { ProjectSaveInput, UploadDocument } from "../types/documents";

type ProcessingRouteState = {
  files?: UploadDocument[];
  projectInfo?: ProjectSaveInput;
  projectId?: number;
};

export function ProcessingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const {
    uploadedFiles,
    startAIProcessing,
    isAIProcessing,
    processingLogs,
    currentDocument,
    activeProjectData,
  } = usePrototype();
  const routeState = location.state as ProcessingRouteState | null;

  const filesToProcess =
    routeState?.files && routeState.files.length > 0
      ? routeState.files
      : activeProjectData?.files || uploadedFiles;

  const projectInfo = routeState?.projectInfo || activeProjectData?.projectInfo;
  const projectId = routeState?.projectId || activeProjectData?.projectId;
  const latestLog = processingLogs[processingLogs.length - 1];
  const latestLogStatus = latestLog?.toLowerCase() || "";
  const hasGeneratedResult = Boolean(
    currentDocument &&
      (currentDocument.file_urls.length > 0 || currentDocument.tableRows.length > 0),
  );
  const isDone = Boolean(
    !isAIProcessing &&
      (hasGeneratedResult ||
        (processingLogs.length > 0 &&
          (latestLogStatus.includes("conclu") || latestLogStatus.includes("[done]")))),
  );
  const hasError = Boolean(
    !isAIProcessing &&
      processingLogs.length > 0 &&
      (latestLogStatus.includes("erro") || latestLogStatus.includes("falha")),
  );
  const canStartManually = Boolean(projectId && projectInfo && !isAIProcessing);

  useEffect(() => {
    if (!isDone) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      navigate("/resultado", { replace: true });
    }, 900);

    return () => window.clearTimeout(timeoutId);
  }, [isDone, navigate]);

  const handleStartManual = () => {
    if (projectId && projectInfo && !isAIProcessing) {
      startAIProcessing(projectId, projectInfo, filesToProcess);
    }
  };

  if (filesToProcess.length === 0 && !isAIProcessing && !isDone && !currentDocument) {
    return (
      <main className="page">
        <div className="page__content page__content--narrow">
          <EmptyState
            tone="error"
            icon={<InfoCircleIcon />}
            title="Nenhum arquivo pronto para processamento"
            description="Adicione ao menos um documento na tela inicial para iniciar o fluxo do EchoCAD."
            actionLabel="Voltar para Home"
            onAction={() => navigate("/")}
          />
        </div>
      </main>
    );
  }

  const title = hasError
    ? "Não foi possível concluir o processamento"
    : isDone
      ? "Processamento concluído"
      : isAIProcessing
        ? "Seu projeto está sendo processado"
        : "Processamento pronto para iniciar";

  const description = hasError
    ? "Ocorreu uma falha durante a geração dos arquivos. Tente novamente ou volte para a tela de resultados."
    : isDone
      ? "Tudo pronto. Abrindo a tela de resultados..."
      : isAIProcessing
        ? "Estamos analisando os arquivos e preparando os documentos finais. Isso pode levar alguns instantes."
        : "Inicie o processamento para gerar os documentos finais do projeto.";

  return (
    <main className="page">
      <div className="page__content page__content--processing">
        <section
          className="processing-card"
          aria-busy={isAIProcessing}
          aria-labelledby="processing-title"
        >
          <div
            className="processing-loader"
            data-state={isDone ? "done" : hasError ? "error" : "loading"}
            aria-hidden="true"
          >
            {isDone || hasError ? (
              isDone ? <CheckCircleIcon /> : <InfoCircleIcon />
            ) : (
              <>
                <span className="processing-loader__ring processing-loader__ring--outer" />
                <span className="processing-loader__ring processing-loader__ring--middle" />
                <span className="processing-loader__ring processing-loader__ring--inner" />
                <span className="processing-loader__dot processing-loader__dot--one" />
                <span className="processing-loader__dot processing-loader__dot--two" />
                <span className="processing-loader__dot processing-loader__dot--three" />
              </>
            )}
          </div>

          <div className="processing-message" role="status" aria-live="polite">
            <h1 id="processing-title" className="processing-message__title">
              {title}
            </h1>
            <p className="processing-message__description">{description}</p>
            {latestLog ? (
              <p className="processing-message__log">{latestLog}</p>
            ) : null}
          </div>

          {hasError || (!isAIProcessing && !isDone) ? (
            <div className="processing-actions">
              {hasError ? (
                <Button variant="secondary" onClick={() => navigate("/resultado")}>
                  Voltar para resultados
                </Button>
              ) : null}
              {canStartManually ? (
                <Button variant="primary" onClick={handleStartManual}>
                  Iniciar processamento
                </Button>
              ) : null}
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}
