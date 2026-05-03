import { useEffect, useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import {
  CheckCircleIcon,
  DownloadIcon,
  InfoCircleIcon,
  SpinnerIcon,
} from "../components/Icons";
import { PreviewPanel } from "../components/PreviewPanel";
import { ProjectSaveModal } from "../components/ProjectSaveModal";
import { SectionTitle } from "../components/SectionTitle";
import { usePrototype } from "../providers/PrototypeProvider";
import { ProjectSaveInput } from "../types/documents";

// Exibe o documento gerado e as ações de download.
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
  } = usePrototype();
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const refreshedIds = useRef<Set<number>>(new Set());

  const routeState = location.state as { refresh?: boolean; projectId?: number } | null;

  useEffect(() => {
    const handleInitialLoad = async () => {
      // Prioridade 1: Refresh solicitado via navegação (ex: após criar projeto)
      if (routeState?.refresh && routeState.projectId && !refreshedIds.current.has(routeState.projectId)) {
        const pid = routeState.projectId;
        refreshedIds.current.add(pid);
        setIsRefreshing(true);
        await refreshCurrentDocument(pid);
        setIsRefreshing(false);
        // Limpamos o state da localização para evitar refresh em re-renders futuros
        navigate(location.pathname, { replace: true, state: {} });
        return;
      } 
      
      // Prioridade 2: Documento atual sem resultados (carregado via histórico ou refresh de página)
      if (currentDocument && currentDocument.file_urls.length === 0 && currentDocument.tableRows.length === 0) {
         const projectId = parseInt(currentDocument.id);
         if (!isNaN(projectId) && !refreshedIds.current.has(projectId)) {
            refreshedIds.current.add(projectId);
            refreshCurrentDocument(projectId);
         }
      }
    };

    handleInitialLoad();
  }, [routeState, currentDocument, refreshCurrentDocument, navigate, location.pathname]);

  useEffect(() => {
    if (
      currentDocument &&
      shouldPromptProjectSave &&
      !currentDocument.projectInfo
    ) {
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

  const handleStartProcessing = () => {
    if (!currentDocument) return;
    const projectId = parseInt(currentDocument.id);
    if (isNaN(projectId)) return;

    const projectInfo: ProjectSaveInput = {
      name: currentDocument.projectInfo?.name || currentDocument.title.replace("Memorial de cálculo - ", ""),
      cliente: currentDocument.projectInfo?.cliente,
      descricao: currentDocument.projectInfo?.descricao || currentDocument.summary,
    };

    // Os arquivos originais podem não estar disponíveis se vier do histórico
    // mas o backend já os tem. Passamos lista vazia se necessário.
    startAIProcessing(projectId, projectInfo, []);
    navigate("/processando");
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
  const isPending = fileUrls.length === 0 && currentDocument.tableRows.length === 0;

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
          <div className={`result-hero__icon${isPending ? " result-hero__icon--pending" : ""}`} aria-hidden="true">
            {isPending ? <InfoCircleIcon /> : <CheckCircleIcon />}
          </div>
          <SectionTitle
            className="result-hero__heading"
            eyebrow="Resultado"
            titleId="result-title"
            title={isPending ? "Processamento pendente" : "Processamento concluído"}
            description={isPending 
              ? "Este projeto ainda não foi processado pela IA. Clique no botão abaixo para iniciar."
              : "Os dados foram analisados com sucesso e o memorial está pronto para exportação."}
            align="center"
          />
        </section>

        <PreviewPanel document={currentDocument} />

        <div className="result-actions">
          {isPending ? (
            <Button 
              variant="primary" 
              onClick={handleStartProcessing}
              disabled={isAIProcessing}
            >
              {isAIProcessing ? "Processando..." : "Iniciar processamento agora"}
            </Button>
          ) : (
            fileUrls.map((url, index) => (
              <Button
                key={`${url}-${index}`}
                variant="primary"
                leadingIcon={<DownloadIcon />}
                onClick={() =>
                  downloadDocumentAsset(url, `memorial-${index + 1}.xlsx`)
                }
              >
                Baixar XLSX
              </Button>
            ))
          )}

          <Button variant="secondary" onClick={() => setShowProjectForm(true)}>
            {currentDocument.projectInfo
              ? "Editar informações"
              : "Salvar projeto"}
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
