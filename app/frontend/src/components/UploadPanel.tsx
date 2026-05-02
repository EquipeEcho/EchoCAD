import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { usePrototype } from "../providers/PrototypeProvider";
import { UploadDocument, UploadStatusTone } from "../types/documents";
import { Button } from "./Button";
import { ConfirmationModal } from "./ConfirmationModal";
import { FileList } from "./FileList";
import { FileRow } from "./FileRow";
import {
  ChevronPlayIcon,
  EyeIcon,
  InfoCircleIcon,
  TrashIcon,
  UploadIcon,
} from "./Icons";

// Monta a mensagem de status apos selecionar arquivos.
function buildUploadStatusMessage(
  addedCount: number,
  duplicateCount: number,
  invalidCount: number,
  totalCount: number
) {
  if (addedCount > 0) {
    return {
      message:
        totalCount === 1
          ? "Arquivo selecionado"
          : `${totalCount} arquivos selecionados`,
      tone: "success" as UploadStatusTone,
    };
  }

  if (invalidCount > 0) {
    return {
      message: "Somente arquivos PDF, DWG, DXF e XML são aceitos.",
      tone: "error" as UploadStatusTone,
    };
  }

  if (duplicateCount > 0) {
    return {
      message: "Os arquivos selecionados já estavam na lista.",
      tone: "info" as UploadStatusTone,
    };
  }

  return {
    message: "Formatos aceitos: PDF, DWG, DXF e XML.",
    tone: "info" as UploadStatusTone,
  };
}

// Controla a selecao e o envio dos arquivos do frontend.
export function UploadPanel() {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [statusMessage, setStatusMessage] = useState(
    "Formatos aceitos: PDF, DWG, DXF e XML."
  );
  const [statusTone, setStatusTone] = useState<UploadStatusTone>("info");
  const [filePendingRemoval, setFilePendingRemoval] =
    useState<UploadDocument | null>(null);
  const [showSendConfirmation, setShowSendConfirmation] = useState(false);
  const {
    uploadedFiles,
    addUploadedFiles,
    removeUploadedFile,
    simulatePreviewAction,
    showToast,
  } = usePrototype();

  // Processa os arquivos escolhidos e atualiza o status.
  const applyFileSelection = (files: FileList | File[]) => {
    const result = addUploadedFiles(files);
    const nextTotalCount = uploadedFiles.length + result.addedCount;
    const nextStatus = buildUploadStatusMessage(
      result.addedCount,
      result.duplicateCount,
      result.invalidCount,
      nextTotalCount
    );

    setStatusMessage(nextStatus.message);
    setStatusTone(nextStatus.tone);

    if (result.addedCount > 0) {
      showToast(
        result.addedCount === 1
          ? "Arquivo adicionado com sucesso."
          : `${result.addedCount} arquivos adicionados com sucesso.`,
        "success"
      );
    } else if (result.invalidCount > 0) {
      showToast(nextStatus.message, "error");
    }
  };

  // Abre o seletor nativo de arquivos.
  const openFilePicker = () => {
    if (!inputRef.current) {
      return;
    }

    inputRef.current.value = "";
    inputRef.current.click();
  };

  // Trata arquivos escolhidos pelo input.
  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    applyFileSelection(event.target.files);
  };

  // Trata arquivos soltos na area de upload.
  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    applyFileSelection(event.dataTransfer.files);
  };

  // Remove o arquivo apos confirmacao do usuario.
  const handleRemoveConfirm = () => {
    if (!filePendingRemoval) {
      return;
    }

    removeUploadedFile(filePendingRemoval.id);
    showToast("Arquivo removido da lista.", "info");
    setFilePendingRemoval(null);
  };

  // Envia os arquivos selecionados para o backend.
  const handleSendConfirm = () => {
    setShowSendConfirmation(false);

    if (uploadedFiles.length === 0) {
      showToast("Nenhum arquivo selecionado.", "error");
      return;
    }

    // envia os arquivos para a próxima página
    navigate("/processando", {
      state: { files: uploadedFiles }
    });
  };

  return (
    <section className="upload-column" aria-labelledby="upload-title">
      <div className="section-heading">
        <p className="section-heading__eyebrow" id="upload-title">
          ÁREA DE UPLOAD
        </p>
      </div>

      <input
        ref={inputRef}
        className="upload-panel__input"
        type="file"
        accept=".dwg,.dxf,.pdf,.xml"
        multiple
        onChange={handleInputChange}
      />

      {uploadedFiles.length === 0 ? (
        <div
          className={`upload-empty${isDragging ? " is-dragging" : ""}`}
          onClick={openFilePicker}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          role="button"
          tabIndex={0}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              openFilePicker();
            }
          }}
        >
          <div className="upload-empty__icon" aria-hidden="true">
            <UploadIcon />
          </div>
          <p className="upload-empty__title">Envie seus arquivos técnicos</p>
          <p className="upload-empty__description">
            Arraste documentos CAD ou clique para selecionar arquivos do computador.
          </p>
          <Button variant="primary" size="lg" onClick={openFilePicker}>
            Selecionar arquivos
          </Button>
        </div>
      ) : (
        <>
          <FileList
            header={
              <div className="file-list-card__header-row">
                <p className="file-list-card__title">
                  {uploadedFiles.length} arquivos selecionados
                </p>
                <button
                  className="text-action"
                  type="button"
                  onClick={openFilePicker}
                >
                  + Adicionar mais
                </button>
              </div>
            }
          >
            <div className="stack">
              {uploadedFiles.map((document) => (
                <FileRow
                  key={document.id}
                  name={document.name}
                  kind={document.kind}
                  actions={[
                    {
                      label: `Visualizar ${document.name}`,
                      icon: <EyeIcon />,
                      onClick: () => simulatePreviewAction(document.name),
                    },
                    {
                      label: `Remover ${document.name}`,
                      icon: <TrashIcon />,
                      onClick: () => setFilePendingRemoval(document),
                      tone: "danger",
                    },
                  ]}
                />
              ))}
            </div>
          </FileList>

          <div className="upload-actions">
            <p
              aria-live="polite"
              className={`status-note status-note--${statusTone}`}
              role="status"
            >
              <span className="status-note__icon" aria-hidden="true">
                <InfoCircleIcon />
              </span>
              <span>{statusMessage}</span>
            </p>

            <div className="upload-actions__buttons">
              <Button variant="primary" onClick={openFilePicker}>
                Adicionar arquivos
              </Button>
              <Button
                variant="success"
                trailingIcon={<ChevronPlayIcon />}
                onClick={() => setShowSendConfirmation(true)}
              >
                Iniciar processamento
              </Button>
            </div>
          </div>
        </>
      )}

      <ConfirmationModal
        open={Boolean(filePendingRemoval)}
        title="Remover arquivo"
        description={
          <p>
            Deseja remover <strong>{filePendingRemoval?.name}</strong> da lista de
            upload?
          </p>
        }
        confirmLabel="Remover"
        onClose={() => setFilePendingRemoval(null)}
        onConfirm={handleRemoveConfirm}
      />

      <ConfirmationModal
        open={showSendConfirmation}
        title="Iniciar processamento"
        description={
          <p>
            Você está prestes a processar {uploadedFiles.length} documento(s). Deseja
            continuar?
          </p>
        }
        confirmLabel="Iniciar"
        confirmTone="success"
        onClose={() => setShowSendConfirmation(false)}
        onConfirm={handleSendConfirm}
      />
    </section>
  );
}
