import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import {
  CheckCircleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  InfoCircleIcon,
  SpinnerIcon,
} from "../components/Icons";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
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

  const [showLogs, setShowLogs] = useState(true);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [processingLogs]);

  const latestLog = processingLogs[processingLogs.length - 1];
  const latestLogStatus = latestLog?.toLowerCase() || "";
  const isDone = Boolean(
    !isAIProcessing &&
      ((processingLogs.length > 0 &&
        (latestLogStatus.includes("conclu") || latestLogStatus.includes("[done]"))) ||
        (currentDocument &&
          (currentDocument.file_urls.length > 0 || currentDocument.tableRows.length > 0))),
  );

  const statusLabel = isDone
    ? "Análise finalizada"
    : isAIProcessing
      ? "Processamento em execução"
      : "Aguardando início";

  const handleStartManual = () => {
    if (projectId && projectInfo && !isAIProcessing) {
      startAIProcessing(projectId, projectInfo, filesToProcess);
    }
  };

  if (filesToProcess.length === 0 && !isAIProcessing) {
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

  return (
    <main className="page">
      <div className="page__content page__content--processing">
        <SurfaceCard
          as="section"
          className="processing-card"
          aria-labelledby="processing-title"
        >
          <SectionTitle
            className="processing-card__heading"
            eyebrow="Processamento"
            titleId="processing-title"
            title={isDone ? "Processamento concluído" : "Processamento em andamento"}
            description={
              isDone
                ? "A análise terminou e os arquivos finais podem ser acessados na tela de resultados."
                : "Acompanhe o estado atual pelos eventos recebidos do backend."
            }
            align="center"
          />

          <div className="processing-status" data-state={isDone ? "done" : isAIProcessing ? "active" : "idle"}>
            <div className="processing-status__icon" aria-hidden="true">
              {isDone ? <CheckCircleIcon /> : isAIProcessing ? <SpinnerIcon className="spin" /> : <InfoCircleIcon />}
            </div>
            <div>
              <p className="processing-status__label">{statusLabel}</p>
              <p className="processing-status__detail">
                {latestLog || "Nenhum evento recebido ainda."}
              </p>
            </div>
          </div>

          <div className="processing-logs-container">
            <button
              className="processing-logs-toggle"
              onClick={() => setShowLogs(!showLogs)}
            >
              {showLogs ? <ChevronUpIcon /> : <ChevronDownIcon />}
              <span>{showLogs ? "Ocultar" : "Ver"} log de processamento da IA</span>
            </button>

            {showLogs && (
              <div className="processing-logs">
                {processingLogs.length === 0 ? (
                  <p className="processing-logs__empty">Aguardando início do pipeline...</p>
                ) : null}
                {processingLogs.map((log, index) => (
                  <div key={`${log}-${index}`} className="processing-logs__item">
                    {log}
                  </div>
                ))}
                <div ref={logsEndRef} />
              </div>
            )}
          </div>

          <div className="processing-actions">
            {!isDone ? (
              <>
                <Button variant="secondary" onClick={() => navigate("/")}>
                  Minimizar e ir para Home
                </Button>
                {!isAIProcessing ? (
                  <Button variant="primary" onClick={handleStartManual}>
                    Iniciar agora
                  </Button>
                ) : null}
              </>
            ) : (
              <>
                <Button variant="secondary" onClick={() => navigate("/")}>
                  Voltar para Home
                </Button>
                <Button variant="success" onClick={() => navigate("/resultado")}>
                  Ver resultados
                </Button>
              </>
            )}
          </div>
        </SurfaceCard>
      </div>
    </main>
  );
}
