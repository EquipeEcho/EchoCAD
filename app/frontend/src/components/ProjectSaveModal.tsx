import { FormEvent, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { GeneratedDocument, ProjectSaveInput } from "../types/documents";
import { getTodayInputValue } from "../utils/date";
import { Button } from "./Button";
import { CloseIcon } from "./Icons";
import { SurfaceCard } from "./SurfaceCard";

type ProjectSaveModalProps = {
  open: boolean;
  document: GeneratedDocument;
  onClose: () => void;
  onSave: (projectInfo: ProjectSaveInput) => void;
};

function getInitialProjectName(document: GeneratedDocument) {
  if (document.projectInfo?.name) {
    return document.projectInfo.name;
  }

  const titleParts = document.title.split(" - ");
  return titleParts.length > 1 ? titleParts.slice(1).join(" - ") : document.title;
}

// Coleta os dados usados para salvar o projeto no histórico.
export function ProjectSaveModal({
  open,
  document: generatedDocument,
  onClose,
  onSave,
}: ProjectSaveModalProps) {
  const titleId = useId();
  const descriptionId = useId();
  const [name, setName] = useState("");
  const [projectDate, setProjectDate] = useState(getTodayInputValue());
  const [responsible, setResponsible] = useState("");
  const [notes, setNotes] = useState("");

  useEffect(() => {
    if (!open) {
      return;
    }

    setName(getInitialProjectName(generatedDocument));
    setProjectDate(generatedDocument.projectInfo?.projectDate || getTodayInputValue());
    setResponsible(generatedDocument.projectInfo?.responsible || "");
    setNotes(generatedDocument.projectInfo?.notes || "");
  }, [generatedDocument, open]);

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

  const canSave = name.trim().length > 0 && projectDate.length > 0;

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!canSave) {
      return;
    }

    onSave({
      name,
      projectDate,
      responsible,
      notes,
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
          <div>
            <h2 className="modal-card__title" id={titleId}>
              Informações do projeto
            </h2>
            <p className="project-save-modal__subtitle" id={descriptionId}>
              Defina como este processamento deve aparecer no histórico.
            </p>
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

          <div className="project-form__grid">
            <label className="form-field">
              <span className="form-field__label">Data do projeto</span>
              <input
                className="form-field__control"
                type="date"
                value={projectDate}
                onChange={(event) => setProjectDate(event.target.value)}
                required
              />
            </label>

            <label className="form-field">
              <span className="form-field__label">Responsável</span>
              <input
                className="form-field__control"
                type="text"
                value={responsible}
                onChange={(event) => setResponsible(event.target.value)}
                placeholder="Nome ou equipe"
              />
            </label>
          </div>

          <label className="form-field">
            <span className="form-field__label">Observações</span>
            <textarea
              className="form-field__control form-field__control--textarea"
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              placeholder="Detalhes para identificar o projeto depois"
              rows={4}
            />
          </label>

          <div className="modal-card__actions">
            <Button variant="ghost" onClick={onClose}>
              Depois
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
