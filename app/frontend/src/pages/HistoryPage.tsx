import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { ConfirmationModal } from "../components/ConfirmationModal";
import { EmptyState } from "../components/EmptyState";
import { DownloadIcon, EyeIcon, InfoCircleIcon, TrashIcon } from "../components/Icons";
import { FileList } from "../components/FileList";
import { FileRow } from "../components/FileRow";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";
import { HistoryDocument } from "../types/documents";

// Lista os documentos gerados anteriormente.
export function HistoryPage() {
  const navigate = useNavigate();
  const {
    historyDocuments,
    downloadDocumentAsset,
    downloadHistoryBundle,
    openHistoryPreview,
    removeHistoryDocument,
  } = usePrototype();
  const [pendingRemoval, setPendingRemoval] = useState<HistoryDocument | null>(null);
  const [confirmBundleDownload, setConfirmBundleDownload] = useState(false);

  // Abre o documento escolhido na tela de resultado.
  const handleOpenPreview = (documentId: string) => {
    openHistoryPreview(documentId);
    navigate("/resultado");
  };

  // Confirma a remocao do item selecionado.
  const handleRemove = () => {
    if (!pendingRemoval) {
      return;
    }

    removeHistoryDocument(pendingRemoval.id);
    setPendingRemoval(null);
  };

  // Dispara o download do pacote completo do historico.
  const handleBundleDownload = () => {
    downloadHistoryBundle();
    setConfirmBundleDownload(false);
  };

  return (
    <main className="page">
      <div className="page__content history-page">
        <SectionTitle
          eyebrow="Histórico"
          title="Histórico de Gerações"
          description="Acompanhe os memoriais e arquivos gerados ao longo das simulações do protótipo."
          actions={
            historyDocuments.length > 0 ? (
              <Button
                variant="secondary"
                leadingIcon={<DownloadIcon />}
                onClick={() => setConfirmBundleDownload(true)}
              >
                Baixar Todos
              </Button>
            ) : null
          }
        />

        <SurfaceCard as="section" className="history-surface">
          {historyDocuments.length === 0 ? (
            <EmptyState
              icon={<InfoCircleIcon />}
              title="Nenhum documento gerado até o momento"
              description="Adicione dados na tela inicial para criar o primeiro memorial no histórico."
              actionLabel="Adicionar dados"
              onAction={() => navigate("/")}
            />
          ) : (
            <>
              <FileList
                className="history-list"
                header={
                  <div className="history-columns" aria-hidden="true">
                    <span>Arquivo</span>
                    <span>Data</span>
                    <span>Tamanho</span>
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
                          label: `Baixar ${document.name}`,
                          icon: <DownloadIcon />,
                          onClick: () => downloadDocumentAsset(document.name, document.document.file_urls[0]), // Usando a URL do arquivo para download
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
          title="Remover documento"
          description={
            <p>
              Deseja remover <strong>{pendingRemoval?.name}</strong> do histórico?
            </p>
          }
          confirmLabel="Remover"
          onClose={() => setPendingRemoval(null)}
          onConfirm={handleRemove}
        />

        <ConfirmationModal
          open={confirmBundleDownload}
          title="Baixar todos os documentos"
          description={
            <p>
              Vamos preparar os itens do histórico para download em um pacote
              único. Deseja continuar?
            </p>
          }
          confirmLabel="Baixar"
          confirmTone="success"
          onClose={() => setConfirmBundleDownload(false)}
          onConfirm={handleBundleDownload}
        />
      </div>
    </main>
  );
}
