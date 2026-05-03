import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import { ChevronDownIcon, ChevronUpIcon, InfoCircleIcon } from "../components/Icons";
import { ProgressIndicator } from "../components/ProgressIndicator";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";
import { ProjectSaveInput, UploadDocument } from "../types/documents";

type ProcessingRouteState = {
  files?: UploadDocument[];
  projectInfo?: ProjectSaveInput;
  projectId?: number;
};

// Mostra o andamento do processamento com feedback da IA.
export function ProcessingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { 
    uploadedFiles, 
    startAIProcessing, 
    isAIProcessing, 
    processingLogs,
    currentDocument,
    activeProjectData
  } = usePrototype();
  const routeState = location.state as ProcessingRouteState | null;
  
  // Usar dados da rota ou os dados ativos no context (persistência se o usuário navegar e voltar)
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
            description="Adicione ao menos um documento na tela inicial para simular o fluxo do EchoCAD."
            actionLabel="Voltar para Home"
            onAction={() => navigate("/")}
          />
        </div>
      </main>
    );
  }

  const isDone = !isAIProcessing && (
    (processingLogs.length > 0 && (
      processingLogs[processingLogs.length - 1].includes("concluído") || 
      processingLogs[processingLogs.length - 1].includes("[DONE]")
    )) || 
    (currentDocument && (currentDocument.file_urls.length > 0 || currentDocument.tableRows.length > 0))
  );

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
            title={isDone ? "Processamento concluído!" : "Aguarde enquanto seus dados são processados"}
            description={isDone 
                ? "A IA finalizou a análise técnica das plantas." 
                : "Estamos analisando os arquivos técnicos em tempo real via Ollama."}
            align="center"
          />

          {!isDone && <ProgressIndicator progress={isAIProcessing ? 65 : 0} />}

          <p className="processing-card__meta">
            {isAIProcessing 
                ? "Processamento ativo no motor de IA..." 
                : isDone ? "Análise finalizada com sucesso." : "Aguardando início..."}
          </p>

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
                {processingLogs.length === 0 && <p className="processing-logs__empty">Aguardando início do pipeline...</p>}
                {processingLogs.map((log, index) => (
                  <div key={index} className="processing-logs__item">
                    {log}
                  </div>
                ))}
                <div ref={logsEndRef} />
              </div>
            )}
          </div>

          <div className="processing-actions" style={{ marginTop: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
             {!isDone && (
                <>
                  <Button variant="secondary" onClick={() => navigate("/")}>
                    Minimizar e ir para Home
                  </Button>
                  {!isAIProcessing && (
                    <Button variant="primary" onClick={handleStartManual}>
                      Iniciar agora
                    </Button>
                  )}
                </>
             )}
             
             {isDone && (
                <>
                  <Button variant="secondary" onClick={() => navigate("/")}>
                    Voltar para Home
                  </Button>
                  <Button variant="success" onClick={() => navigate("/resultado")}>
                      Ver Resultados
                  </Button>
                </>
             )}
          </div>
        </SurfaceCard>
      </div>
    </main>
  );
}
