import { FormEvent, useEffect, useId, useState } from "react";
import { createPortal } from "react-dom";
import { Button } from "./Button";
import { CloseIcon, InfoCircleIcon } from "./Icons";
import { SurfaceCard } from "./SurfaceCard";

export interface PlantaCADInfo {
  tipo: string;
  arquivo: string;
}

type PlantaCADModalProps = {
  open: boolean;
  onClose: () => void;
  onSave: (plantaInfo: PlantaCADInfo) => void;
};

const PLANT_TYPE_OPTIONS = ["Planta Arquitetura", "Planta Elétrica", "Planta Hidráulica", "Planta Estrutural", "Planta HVAC", "Outra"];

// Coleta os dados da planta CAD a ser salva no projeto.
export function PlantaCADModal({
  open,
  onClose,
  onSave,
}: PlantaCADModalProps) {
  const titleId = useId();
  const descriptionId = useId();
  const [tipo, setTipo] = useState(PLANT_TYPE_OPTIONS[0]);
  const [arquivo, setArquivo] = useState("");

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

  const canSave = tipo.trim().length > 0;

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!canSave) {
      return;
    }

    onSave({
      tipo,
      arquivo,
    });

    onClose();

    // Redefinir formulário
    setTipo(PLANT_TYPE_OPTIONS[0]);
    setArquivo("");
  };

  return createPortal(
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <SurfaceCard
        as="div"
        className="modal-card project-save-modal plant-cad-modal"
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
              <p className="project-save-modal__eyebrow">Cadastro CAD</p>
              <h2 className="modal-card__title" id={titleId}>
                Informações da Planta CAD
              </h2>
              <p className="project-save-modal__subtitle" id={descriptionId}>
                Defina os detalhes da planta CAD a ser adicionada ao projeto.
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
              <legend className="project-form__section-label">Classificação</legend>

              <div className="form-field">
                <span className="form-field__label">Tipo de planta</span>
                <div className="plant-type-grid" role="radiogroup" aria-label="Tipo de planta">
                  {PLANT_TYPE_OPTIONS.map((option) => (
                    <button
                      className={`plant-type-option${option === tipo ? " is-selected" : ""}`}
                      key={option}
                      type="button"
                      role="radio"
                      aria-checked={option === tipo}
                      onClick={() => setTipo(option)}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </fieldset>
          </div>

          <div className="modal-card__actions">
            <Button variant="ghost" type="button" onClick={onClose}>
              Cancelar
            </Button>
            <Button variant="success" type="submit" disabled={!canSave}>
              Adicionar planta
            </Button>
          </div>
        </form>
      </SurfaceCard>
    </div>,
    document.body
  );
}
