import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { Button } from "../components/Button";
import { EmptyState } from "../components/EmptyState";
import { DownloadIcon, InfoCircleIcon, UploadIcon } from "../components/Icons";
import { FileList } from "../components/FileList";
import { FileRow } from "../components/FileRow";
import { SectionTitle } from "../components/SectionTitle";
import { SurfaceCard } from "../components/SurfaceCard";
import { usePrototype } from "../providers/PrototypeProvider";
import { UploadStatusTone } from "../types/documents";

type StandardSwitchProps = {
  enabled: boolean;
  label: string;
  onToggle: () => void;
};

function buildStandardsUploadStatus(
  addedCount: number,
  duplicateCount: number,
  invalidCount: number
) {
  if (addedCount > 0) {
    return {
      message:
        addedCount === 1
          ? "Norma adicionada e habilitada para consulta."
          : `${addedCount} normas adicionadas e habilitadas para consulta.`,
      tone: "success" as UploadStatusTone,
    };
  }

  if (invalidCount > 0) {
    return {
      message: "Somente normas em PDF são aceitas.",
      tone: "error" as UploadStatusTone,
    };
  }

  if (duplicateCount > 0) {
    return {
      message: "As normas selecionadas já estavam na lista.",
      tone: "info" as UploadStatusTone,
    };
  }

  return {
    message: "Envie novas normas técnicas em PDF.",
    tone: "info" as UploadStatusTone,
  };
}

function StandardSwitch({ enabled, label, onToggle }: StandardSwitchProps) {
  return (
    <button
      className={`standard-switch${enabled ? " is-enabled" : ""}`}
      type="button"
      role="switch"
      aria-checked={enabled}
      aria-label={`${enabled ? "Desabilitar" : "Habilitar"} ${label}`}
      onClick={onToggle}
    >
      <span className="standard-switch__track" aria-hidden="true">
        <span className="standard-switch__thumb" />
      </span>
      <span className="standard-switch__label">
        {enabled ? "Habilitada" : "Desabilitada"}
      </span>
    </button>
  );
}

export function StandardsPage() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(
    buildStandardsUploadStatus(0, 0, 0)
  );
  const {
    addTechnicalStandards,
    downloadStandard,
    technicalStandards,
    toggleStandard,
  } = usePrototype();
  const enabledCount = technicalStandards.filter((standard) => standard.enabled)
    .length;

  const openFilePicker = () => {
    if (!inputRef.current) {
      return;
    }

    inputRef.current.value = "";
    inputRef.current.click();
  };

  const applyStandardsSelection = (files: FileList | File[]) => {
    const result = addTechnicalStandards(files);
    setUploadStatus(
      buildStandardsUploadStatus(
        result.addedCount,
        result.duplicateCount,
        result.invalidCount
      )
    );
  };

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    applyStandardsSelection(event.target.files);
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    applyStandardsSelection(event.dataTransfer.files);
  };

  return (
    <main className="page">
      <div className="page__content history-page standards-page">
        <SectionTitle
          eyebrow="Normas"
          title="Normas técnicas"
          description={`${enabledCount} de ${technicalStandards.length} normas habilitadas para consulta da IA.`}
        />

        <SurfaceCard
          as="section"
          className={`standards-upload${isDragging ? " is-dragging" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          <input
            ref={inputRef}
            className="upload-panel__input"
            type="file"
            accept=".pdf"
            multiple
            onChange={handleInputChange}
          />

          <div className="standards-upload__body">
            <div className="standards-upload__icon" aria-hidden="true">
              <UploadIcon />
            </div>
            <div className="standards-upload__copy">
              <h2 className="standards-upload__title">Adicionar norma técnica</h2>
              <p className="standards-upload__description">
                Arquivos enviados aqui entram habilitados para consulta da IA.
              </p>
            </div>
            <Button
              variant="primary"
              leadingIcon={<UploadIcon />}
              onClick={openFilePicker}
            >
              Enviar norma
            </Button>
          </div>

          <p
            aria-live="polite"
            className={`status-note status-note--${uploadStatus.tone}`}
            role="status"
          >
            <span className="status-note__icon" aria-hidden="true">
              <InfoCircleIcon />
            </span>
            <span>{uploadStatus.message}</span>
          </p>
        </SurfaceCard>

        <SurfaceCard as="section" className="history-surface standards-surface">
          {technicalStandards.length === 0 ? (
            <EmptyState
              icon={<InfoCircleIcon />}
              title="Nenhuma norma cadastrada"
              description="Envie arquivos PDF para montar a biblioteca técnica usada pelo protótipo."
              actionLabel="Enviar norma"
              onAction={openFilePicker}
            />
          ) : (
            <FileList
              className="history-list standards-list"
              header={
                <div className="standards-columns" aria-hidden="true">
                  <span>Norma</span>
                  <span>Área</span>
                  <span>Atualização</span>
                  <span>Consulta IA</span>
                  <span>Ações</span>
                </div>
              }
            >
              <div className="stack">
                {technicalStandards.map((standard) => (
                  <FileRow
                    key={standard.id}
                    variant="standard"
                    name={standard.name}
                    kind={standard.kind}
                    hint={
                      standard.enabled
                        ? "Consultada pela IA"
                        : "Ignorada pela IA"
                    }
                    metaItems={[
                      { label: "Área", value: standard.category },
                      { label: "Atualização", value: standard.date },
                    ]}
                    statusControl={
                      <StandardSwitch
                        enabled={standard.enabled}
                        label={standard.code}
                        onToggle={() => toggleStandard(standard.id)}
                      />
                    }
                    actions={[
                      {
                        label: `Baixar ${standard.name}`,
                        icon: <DownloadIcon />,
                        onClick: () => downloadStandard(standard.id),
                      },
                    ]}
                  />
                ))}
              </div>
            </FileList>
          )}
        </SurfaceCard>
      </div>
    </main>
  );
}
