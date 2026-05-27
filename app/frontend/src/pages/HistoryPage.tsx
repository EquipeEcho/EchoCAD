import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { ConfirmationModal } from "../components/ConfirmationModal";
import { EmptyState } from "../components/EmptyState";
import {
  CloseIcon,
  DownloadIcon,
  EyeIcon,
  InfoCircleIcon,
  SearchIcon,
  TrashIcon,
} from "../components/Icons";
import { FileList } from "../components/FileList";
import { FileRow } from "../components/FileRow";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../hooks/usePrototype";
import { API_BASE_URL, getAuthHeaders } from "../services/api";
import { HistoryDocument } from "../types/documents";

async function downloadFile(url: string, fileName: string) {
  const response = await fetch(url, {
    headers: {
      ...(getAuthHeaders() ?? {}),
    },
  });
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

function normalizeSearchValue(value: string) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function getHistorySearchText(document: HistoryDocument) {
  return [
    document.id,
    document.name,
    document.kind,
    document.date,
    document.projectInfo?.cliente,
    document.projectInfo?.descricao,
    document.document.reference,
    document.document.summary,
  ]
    .filter(Boolean)
    .join(" ");
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
  const [searchQuery, setSearchQuery] = useState("");

  const isDownloading = useMemo(() => {
    return (projectId: string) => downloadingProjectId === projectId;
  }, [downloadingProjectId]);

  const filteredHistoryDocuments = useMemo(() => {
    const normalizedQuery = normalizeSearchValue(searchQuery);

    if (!normalizedQuery) {
      return historyDocuments;
    }

    return historyDocuments.filter((document) =>
      normalizeSearchValue(getHistorySearchText(document)).includes(normalizedQuery),
    );
  }, [historyDocuments, searchQuery]);

  const hasSearchQuery = searchQuery.trim().length > 0;
  const searchResultLabel =
    filteredHistoryDocuments.length === 1
      ? "1 projeto encontrado"
      : `${filteredHistoryDocuments.length} projetos encontrados`;

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
      await downloadFile(
        `${API_BASE_URL}/memorial_calculo/projeto/${projectId}/download`,
        `projeto_${projectId}_memorial_calculo.xlsx`,
      );
      try {
        await downloadFile(
          `${API_BASE_URL}/especificacoes_tecnicas/projeto/${projectId}/download`,
          `projeto_${projectId}_especificacoes_tecnicas.docx`,
        );
      } catch (specError) {
        console.warn("Especificacoes tecnicas indisponiveis para este projeto.", specError);
      }
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

        <SurfaceCard
          as="section"
          className={`history-surface${
            isLoadingHistory || historyError || historyDocuments.length === 0
              ? " history-surface--empty"
              : ""
          }`}
        >
          {isLoadingHistory ? (
            <EmptyState
              framed={false}
              icon={<InfoCircleIcon />}
              title="Carregando projetos..."
              description="Estamos consultando os dados no endpoint de Projeto."
            />
          ) : historyError ? (
            <EmptyState
              framed={false}
              icon={<InfoCircleIcon />}
              title="Não foi possível listar os projetos"
              description={historyError}
              actionLabel="Tentar novamente"
              onAction={() => window.location.reload()}
            />
          ) : historyDocuments.length === 0 ? (
            <EmptyState
              framed={false}
              icon={<InfoCircleIcon />}
              title="Nenhum projeto cadastrado até o momento"
              description="Envie uma planta CAD e salve o projeto para acompanhar os arquivos gerados por aqui."
              actionLabel="Criar projeto"
              onAction={() => navigate("/")}
            />
          ) : (
            <>
              <div className="history-toolbar">
                <label className="history-search">
                  <span className="history-search__icon" aria-hidden="true">
                    <SearchIcon />
                  </span>
                  <span className="sr-only">Buscar projetos no histórico</span>
                  <input
                    className="history-search__input"
                    type="search"
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                    placeholder="Buscar por projeto, cliente, data ou ID"
                  />
                  {hasSearchQuery ? (
                    <button
                      className="history-search__clear"
                      type="button"
                      onClick={() => setSearchQuery("")}
                      aria-label="Limpar busca"
                    >
                      <CloseIcon />
                    </button>
                  ) : null}
                </label>
                <span className="history-toolbar__count">
                  {hasSearchQuery ? searchResultLabel : `${historyDocuments.length} projetos`}
                </span>
              </div>

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
                {filteredHistoryDocuments.length > 0 ? (
                  <div className="stack">
                    {filteredHistoryDocuments.map((document) => (
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
                ) : (
                  <div className="history-search-empty" role="status">
                    <InfoCircleIcon />
                    <p>Nenhum projeto encontrado para esta busca.</p>
                  </div>
                )}
              </FileList>

              <div className="history-surface__footer">
                <Button variant="success" onClick={() => navigate("/")}>
                  Criar projeto
                </Button>
              </div>
            </>
          )}
        </SurfaceCard>
        <ConfirmationModal
          open={Boolean(pendingRemoval)}
          title="Remover projeto"
          description={
            <p>
              Deseja remover <strong>{pendingRemoval?.name}</strong> do histórico?
            </p>
          }
          confirmLabel="Remover"
          confirmTone="danger"
          onClose={() => setPendingRemoval(null)}
          onConfirm={handleRemove}
        />
      </div>
    </main>
  );
}
