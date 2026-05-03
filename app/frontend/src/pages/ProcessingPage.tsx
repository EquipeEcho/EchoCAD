import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { EmptyState } from "../components/EmptyState";
import { InfoCircleIcon } from "../components/Icons";
import { ProgressIndicator } from "../components/ProgressIndicator";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";
import { ProjectSaveInput, UploadDocument } from "../types/documents";
import { processProject } from "../services/api";

const progressSteps = [12, 26, 39, 57, 71, 86, 100];

type ProcessingRouteState = {
  files?: UploadDocument[];
  projectInfo?: ProjectSaveInput;
  projectId?: number;
};

// Mostra o andamento do processamento simulado.
export function ProcessingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { uploadedFiles, completeProcessing } = usePrototype();
  const routeState = location.state as ProcessingRouteState | null;
  const filesToProcess =
    routeState?.files && routeState.files.length > 0
      ? routeState.files
      : uploadedFiles;
  const projectInfo = routeState?.projectInfo;

  const [progress, setProgress] = useState(progressSteps[0]);
  const hasFinishedRef = useRef(false);

  useEffect(() => {
    if (filesToProcess.length === 0) return;

    let stepIndex = 0;
    const intervalId = window.setInterval(() => {
      stepIndex += 1;

      if (stepIndex >= progressSteps.length) {
        window.clearInterval(intervalId);
        return;
      }

      setProgress(progressSteps[stepIndex]);
    }, 520);

    return () => window.clearInterval(intervalId);
  }, [filesToProcess.length]);

  useEffect(() => {
    if (
      progress < 100 ||
      hasFinishedRef.current ||
      filesToProcess.length === 0
    ) {
      return;
    }

    const startActualProcessing = async () => {
      if (hasFinishedRef.current) return;
      hasFinishedRef.current = true;

      try {
        let results = [];
        if (routeState?.projectId) {
          const apiResponse = await processProject(routeState.projectId);
          results = apiResponse.results || [];
        }
        
        completeProcessing(results, projectInfo, filesToProcess);
        navigate("/resultado", { replace: true });
      } catch (error) {
        console.error("Erro no processamento real:", error);
        completeProcessing([], projectInfo, filesToProcess);
        navigate("/resultado", { replace: true });
      }
    };

    const timeoutId = window.setTimeout(() => {
      startActualProcessing();
    }, 500);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [completeProcessing, filesToProcess, navigate, progress, projectInfo, routeState?.projectId]);

  if (filesToProcess.length === 0) {
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

  const expectedTime = filesToProcess.length >= 3 ? "3 minutos" : "2 minutos";

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
            title="Aguarde enquanto seus dados são processados"
            description={`Tempo estimado: ${expectedTime}. Estamos analisando os arquivos técnicos e consolidando o memorial de cálculo.`}
            align="center"
          />

          <ProgressIndicator progress={progress} />

          <p className="processing-card__meta">
            {progress}% concluído com base em dados simulados do protótipo.
          </p>
        </SurfaceCard>
      </div>
    </main>
  );
}
