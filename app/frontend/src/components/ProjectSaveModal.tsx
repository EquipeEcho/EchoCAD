import { FormEvent, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { GeneratedDocument, ProjectSaveInput } from "../types/documents";
import { Button } from "./Button";
import { CloseIcon, InfoCircleIcon } from "./Icons";
import { SurfaceCard } from "./SurfaceCard";

type ProjectSaveModalProps = {
  open: boolean;
  document?: GeneratedDocument;
  initialProjectName?: string;
  subtitle?: string;
  cancelLabel?: string;
  onClose: () => void;
  onSave: (projectInfo: ProjectSaveInput) => void;
};

function getInitialProjectName(
  document: GeneratedDocument | undefined,
  fallbackName: string
) {
  if (document?.projectInfo?.name) {
    return document.projectInfo.name;
  }

  if (document?.title) {
    const titleParts = document.title.split(" - ");
    return titleParts.length > 1
      ? titleParts.slice(1).join(" - ")
      : document.title;
  }

  return fallbackName;
}

// Coleta os dados do projeto de acordo com o modelo da tabela Projeto.
export function ProjectSaveModal({
  open,
  document: generatedDocument,
  initialProjectName = "",
  subtitle = "Defina como este processamento deve aparecer no histórico.",
  cancelLabel = "Depois",
  onClose,
  onSave,
}: ProjectSaveModalProps) {
  const titleId = useId();
  const descriptionId = useId();
  const [name, setName] = useState("");
  const [cliente, setCliente] = useState("");
  const [descricao, setDescricao] = useState("");

  useEffect(() => {
    if (!open) {
      return;
    }

    setName(getInitialProjectName(generatedDocument, initialProjectName));
    setCliente(generatedDocument?.projectInfo?.cliente || "");
    setDescricao(generatedDocument?.projectInfo?.descricao || "");
  }, [generatedDocument, initialProjectName, open]);

  useEffect(() => {
    if (!open) {
      return;
    }

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleEscape);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", handleEscape);
    };
  }, [open, onClose]);

  if (!open) {
    return null;
  }

  const canSave =
    name.trim().length > 0;

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!canSave) {
      return;
    }

    onSave({
      name,
      cliente,
      descricao,
    });
  };

  return createPortal(
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <SurfaceCard
        as="div"
        className="modal-card project-save-modal"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <div className="modal-card__header">
          <div className="project-save-modal__heading">
            <span className="project-save-modal__icon" aria-hidden="true">
              <InfoCircleIcon />
            </span>
            <div>
              <h2 className="modal-card__title" id={titleId}>
                Informações do projeto
              </h2>
              <p className="project-save-modal__subtitle" id={descriptionId}>
                {subtitle}
              </p>
            </div>
          </div>

          <button
            className="modal-card__close"
            type="button"
            onClick={onClose}
            aria-label="Fechar modal"
          >
            <CloseIcon />
          </button>
        </div>

        <form className="project-form" onSubmit={handleSubmit}>
          <div className="project-form__body">
            <fieldset className="project-form__section">
              <legend className="project-form__section-label">Informações do Projeto</legend>

              <label className="form-field">
                <span className="form-field__label">Nome do projeto</span>
                <input
                  className="form-field__control"
                  type="text"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  placeholder="Ex.: Residencial Jardim Sul"
                  required
                />
              </label>

              <label className="form-field">
                <span className="form-field__label">Cliente (opcional)</span>
                <input
                  className="form-field__control"
                  type="text"
                  value={cliente}
                  onChange={(event) => setCliente(event.target.value)}
                  placeholder="Ex.: Construtora ABC Ltda."
                />
              </label>

              <label className="form-field">
                <span className="form-field__label">Descrição (opcional)</span>
                <textarea
                  className="form-field__control form-field__control--textarea form-field__control--textarea-compact"
                  value={descricao}
                  onChange={(event) => setDescricao(event.target.value)}
                  placeholder="Descrição detalhada do projeto"
                  rows={3}
                />
              </label>
            </fieldset>
          </div>

          <div className="modal-card__actions">
            <Button variant="ghost" onClick={onClose}>
              {cancelLabel}
            </Button>
            <Button variant="success" type="submit" disabled={!canSave}>
              Salvar projeto
            </Button>
          </div>
        </form>
      </SurfaceCard>
    </div>,
    document.body
  );
}
