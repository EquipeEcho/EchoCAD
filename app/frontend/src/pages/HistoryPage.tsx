import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { ConfirmationModal } from "../components/ConfirmationModal";
import { EmptyState } from "../components/EmptyState";
import {
  DownloadIcon,
  EyeIcon,
  InfoCircleIcon,
  TrashIcon,
} from "../components/Icons";
import { FileList } from "../components/FileList";
import { FileRow } from "../components/FileRow";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";
import { HistoryDocument } from "../types/documents";

const API_BASE_URL = "http://127.0.0.1:8000";

async function downloadFile(url: string, fileName: string) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Erro ao baixar ${fileName}`);
  }

  const blob = await response.blob();
  const objectUrl = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(objectUrl);
}

export function HistoryPage() {
  const navigate = useNavigate();
  const {
    historyDocuments,
    isLoadingHistory,
    historyError,
    openHistoryPreview,
    removeHistoryDocument,
  } = usePrototype();
  const [pendingRemoval, setPendingRemoval] = useState<HistoryDocument | null>(null);
  const [downloadingProjectId, setDownloadingProjectId] = useState<string | null>(null);

  const isDownloading = useMemo(() => {
    return (projectId: string) => downloadingProjectId === projectId;
  }, [downloadingProjectId]);

  const handleOpenPreview = (documentId: string) => {
    openHistoryPreview(documentId);
    navigate("/resultado");
  };

  const handleRemove = async () => {
    if (!pendingRemoval) {
      return;
    }

    await removeHistoryDocument(pendingRemoval.id);
    setPendingRemoval(null);
  };

  const handleDownloadProjectFiles = async (document: HistoryDocument) => {
    const projectId = Number(document.id);
    if (!Number.isFinite(projectId)) {
      window.alert("ID do projeto inválido para download.");
      return;
    }

    if (downloadingProjectId !== null) {
      return;
    }

    setDownloadingProjectId(document.id);
    try {
      await Promise.all([
        downloadFile(
          `${API_BASE_URL}/especificacao_tecnica/projeto/${projectId}/download`,
          `projeto_${projectId}_especificacoes_tecnicas.py`,
        ),
        downloadFile(
          `${API_BASE_URL}/memorial_calculo/projeto/${projectId}/download`,
          `projeto_${projectId}_memorial_calculo.py`,
        ),
      ]);
    } catch (error) {
      console.error(error);
      window.alert(
        "Não foi possível baixar os arquivos do projeto. Verifique se o backend está online.",
      );
    } finally {
      setDownloadingProjectId(null);
    }
  };

  return (
    <main className="page">
      <div className="page__content history-page">
        <SectionTitle
          eyebrow="Histórico"
          title="Histórico de Projetos"
          description="Lista de todos os projetos cadastrados no banco de dados."
        />

        <SurfaceCard as="section" className="history-surface">
          {isLoadingHistory ? (
            <EmptyState
              icon={<InfoCircleIcon />}
              title="Carregando projetos..."
              description="Estamos consultando os dados no endpoint de Projeto."
            />
          ) : historyError ? (
            <EmptyState
              icon={<InfoCircleIcon />}
              title="Não foi possível listar os projetos"
              description={historyError}
              actionLabel="Tentar novamente"
              onAction={() => window.location.reload()}
            />
          ) : historyDocuments.length === 0 ? (
            <EmptyState
              icon={<InfoCircleIcon />}
              title="Nenhum projeto cadastrado até o momento"
              description="Crie um projeto no backend para que ele apareça nesta lista."
              actionLabel="Adicionar dados"
              onAction={() => navigate("/")}
            />
          ) : (
            <>
              <FileList
                className="history-list"
                header={
                  <div className="history-columns" aria-hidden="true">
                    <span>Projeto</span>
                    <span>Data</span>
                    <span>Detalhe</span>
                    <span>Ações</span>
                  </div>
                }
              >
                <div className="stack">
                  {historyDocuments.map((document) => (
                    <FileRow
                      key={document.id}
                      variant="history"
                      name={document.name}
                      kind={document.kind}
                      date={document.date}
                      size={document.size}
                      actions={[
                        {
                          label: isDownloading(document.id)
                            ? `Baixando arquivos de ${document.name}`
                            : `Baixar arquivos de ${document.name}`,
                          icon: <DownloadIcon />,
                          onClick: () => handleDownloadProjectFiles(document),
                        },
                        {
                          label: `Visualizar ${document.name}`,
                          icon: <EyeIcon />,
                          onClick: () => handleOpenPreview(document.id),
                        },
                        {
                          label: `Remover ${document.name}`,
                          icon: <TrashIcon />,
                          onClick: () => setPendingRemoval(document),
                          tone: "danger",
                        },
                      ]}
                    />
                  ))}
                </div>
              </FileList>

              <div className="history-surface__footer">
                <Button variant="success" onClick={() => navigate("/")}>
                  Adicionar dados
                </Button>
              </div>
            </>
          )}
        </SurfaceCard>
        <ConfirmationModal
          open={Boolean(pendingRemoval)}
          title="Remover projeto da lista"
          description={
            <p>
              Deseja remover <strong>{pendingRemoval?.name}</strong> da lista local?
            </p>
          }
          confirmLabel="Remover"
          onClose={() => setPendingRemoval(null)}
          onConfirm={handleRemove}
        />
      </div>
    </main>
  );
}
