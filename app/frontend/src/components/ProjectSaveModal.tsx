import { FormEvent, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { GeneratedDocument, ProjectSaveInput } from "../types/documents";
import { getTodayInputValue } from "../utils/date";
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

const MODEL_TYPE_OPTIONS = ["Residencial", "Comercial", "Industrial"];

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

// Coleta os dados usados para salvar o projeto no histórico.
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
  const [projectDate, setProjectDate] = useState(getTodayInputValue());
  const [responsible, setResponsible] = useState("");
  const [modelType, setModelType] = useState(MODEL_TYPE_OPTIONS[0]);
  const [notes, setNotes] = useState("");
  const [additionalInstructions, setAdditionalInstructions] = useState("");

  useEffect(() => {
    if (!open) {
      return;
    }

    setName(getInitialProjectName(generatedDocument, initialProjectName));
    setProjectDate(generatedDocument?.projectInfo?.projectDate || getTodayInputValue());
    setResponsible(generatedDocument?.projectInfo?.responsible || "");
    setModelType(generatedDocument?.projectInfo?.modelType || MODEL_TYPE_OPTIONS[0]);
    setNotes(generatedDocument?.projectInfo?.notes || "");
    setAdditionalInstructions(
      generatedDocument?.projectInfo?.additionalInstructions || ""
    );
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
    name.trim().length > 0 && projectDate.length > 0 && modelType.length > 0;

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!canSave) {
      return;
    }

    onSave({
      name,
      projectDate,
      responsible,
      modelType,
      notes,
      additionalInstructions,
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
              <legend className="project-form__section-label">Identificação</legend>

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

              <div className="project-form__grid project-form__grid--three">
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
                  <span className="form-field__label">Tipo de modelo</span>
                  <select
                    className="form-field__control"
                    value={modelType}
                    onChange={(event) => setModelType(event.target.value)}
                    required
                  >
                    {MODEL_TYPE_OPTIONS.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
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
            </fieldset>

            <fieldset className="project-form__section">
              <legend className="project-form__section-label">Contexto da IA</legend>

              <label className="form-field">
                <span className="form-field__label">Observações</span>
                <textarea
                  className="form-field__control form-field__control--textarea form-field__control--textarea-compact"
                  value={notes}
                  onChange={(event) => setNotes(event.target.value)}
                  placeholder="Detalhes para identificar o projeto depois"
                  rows={3}
                />
              </label>

              <label className="form-field">
                <span className="form-field__label">Instruções adicionais</span>
                <textarea
                  className="form-field__control form-field__control--textarea"
                  value={additionalInstructions}
                  onChange={(event) => setAdditionalInstructions(event.target.value)}
                  placeholder="Ex.: Considerar materiais de baixo custo"
                  rows={4}
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
