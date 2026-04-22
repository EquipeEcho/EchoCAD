import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import { CheckCircleIcon, DownloadIcon, InfoCircleIcon } from "../components/Icons";
import { PreviewPanel } from "../components/PreviewPanel";
import { ProjectSaveModal } from "../components/ProjectSaveModal";
import { SectionTitle } from "../components/SectionTitle";
import { usePrototype } from "../providers/PrototypeProvider";
import { ProjectSaveInput } from "../types/documents";

// Exibe o documento gerado e as ações de download.
export function ResultPage() {
  const navigate = useNavigate();
  const {
    currentDocument,
    downloadDocumentAsset,
    saveCurrentProject,
    shouldPromptProjectSave,
  } = usePrototype();
  const [showProjectForm, setShowProjectForm] = useState(false);

  useEffect(() => {
    if (currentDocument && shouldPromptProjectSave && !currentDocument.projectInfo) {
      setShowProjectForm(true);
    }
  }, [currentDocument, shouldPromptProjectSave]);

  // Volta para a tela anterior ou para a home.
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

  const fileUrls = currentDocument.file_urls;

  return (
    <main className="page">
      <div className="page__content page__content--result">
        <section className="result-hero" aria-labelledby="result-title">
          <div className="result-hero__icon" aria-hidden="true">
            <CheckCircleIcon />
          </div>
          <SectionTitle
            className="result-hero__heading"
            eyebrow="Resultado"
            titleId="result-title"
            title="Processamento concluído"
            description="Os dados foram analisados com sucesso e o memorial está pronto para exportação."
            align="center"
          />
        </section>

        <PreviewPanel document={currentDocument} />

        <div className="result-actions">
          <Button variant="secondary" onClick={() => setShowProjectForm(true)}>
            {currentDocument.projectInfo ? "Editar informações" : "Salvar projeto"}
          </Button>

          {fileUrls.map((url, index) => (
            <Button
              key={url}
              variant="primary"
              leadingIcon={<DownloadIcon />}
              onClick={() =>
                downloadDocumentAsset(url, `memorial-${index + 1}.xlsx`)
              }
            >
              Baixar XLSX
            </Button>
          ))}

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
