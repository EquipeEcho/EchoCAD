import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { EmptyState } from "../components/EmptyState";
import { InfoCircleIcon } from "../components/Icons";
import { ProgressIndicator } from "../components/ProgressIndicator";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";

const progressSteps = [12, 26, 39, 57, 71, 86, 100];

// Mostra o andamento do processamento simulado.
export function ProcessingPage() {
  const navigate = useNavigate();
  const { uploadedFiles, completeProcessing } = usePrototype();

  const [progress, setProgress] = useState(progressSteps[0]);
  const [results, setResults] = useState<any[]>([]);
  const [isProcessingDone, setIsProcessingDone] = useState(false);

  const hasFinishedRef = useRef(false);
  const hasStartedRef = useRef(false);

  useEffect(() => {
    if (uploadedFiles.length === 0) return;

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
  }, [uploadedFiles.length]);

  useEffect(() => {
    if (uploadedFiles.length === 0 || hasStartedRef.current) return;

    hasStartedRef.current = true;

    const processFiles = async () => {
      try {
        const doc = uploadedFiles[0];

        const formData = new FormData();
        formData.append("file", doc.file);

        const response = await fetch("http://127.0.0.1:8000/upload/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Erro no envio");
        }

        const blob = await response.blob();
        const fileUrl = URL.createObjectURL(blob);

        const apiResults = [{ file_url: fileUrl }];

        completeProcessing(apiResults);
        setIsProcessingDone(true);

      } catch (error) {
        console.error(error);
        navigate("/", { replace: true });
      }
    };

    processFiles();
  }, [uploadedFiles, navigate]);

  useEffect(() => {
    if (
      progress < 100 ||
      !isProcessingDone ||
      hasFinishedRef.current
    ) {
      return;
    }

    hasFinishedRef.current = true;

    navigate("/resultado", {
      replace: true,
      state: { results }
    });

  }, [progress, isProcessingDone, results, navigate]);

  if (uploadedFiles.length === 0) {
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

  const expectedTime = uploadedFiles.length >= 3 ? "3 minutos" : "2 minutos";

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
            description={`Tempo esperado: ${expectedTime}. Estamos analisando os arquivos técnicos e consolidando o memorial de cálculo.`}
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
