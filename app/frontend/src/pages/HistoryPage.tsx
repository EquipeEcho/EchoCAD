import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { ConfirmationModal } from "../components/ConfirmationModal";
import { EmptyState } from "../components/EmptyState";
import {
  CloseIcon,
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
import { HistoryDocument } from "../types/documents";

function normalizeSearchValue(value: string) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function getHistorySearchFields(document: HistoryDocument) {
  return [
    document.name,
    document.projectInfo?.cliente,
    document.date,
    document.id,
  ].filter(Boolean);
}

function matchesHistorySearch(document: HistoryDocument, normalizedQuery: string) {
  const queryTerms = normalizedQuery.split(/\s+/).filter(Boolean);

  if (queryTerms.length === 0) {
    return true;
  }

  const searchableFields = getHistorySearchFields(document).map((value) =>
    normalizeSearchValue(String(value)),
  );

  return queryTerms.every((term) =>
    searchableFields.some((field) => field.includes(term)),
  );
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
  const [searchQuery, setSearchQuery] = useState("");

  const filteredHistoryDocuments = useMemo(() => {
    const normalizedQuery = normalizeSearchValue(searchQuery);

    if (!normalizedQuery) {
      return historyDocuments;
    }

    return historyDocuments.filter((document) =>
      matchesHistorySearch(document, normalizedQuery),
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
