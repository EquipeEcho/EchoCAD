import { ReactNode, useEffect, useId } from "react";
import { createPortal } from "react-dom";
import { Button } from "./Button";
import { CloseIcon } from "./Icons";
import { SurfaceCard } from "./SurfaceCard";

type ConfirmationModalProps = {
  open: boolean;
  title: string;
  description: ReactNode;
  confirmLabel: string;
  cancelLabel?: string;
  confirmTone?: "primary" | "success";
  onClose: () => void;
  onConfirm: () => void;
};

// Exibe uma confirmação antes de ações sensíveis.
export function ConfirmationModal({
  open,
  title,
  description,
  confirmLabel,
  cancelLabel = "Cancelar",
  confirmTone = "primary",
  onClose,
  onConfirm,
}: ConfirmationModalProps) {
  const titleId = useId();
  const descriptionId = useId();

  useEffect(() => {
    if (!open) {
      return;
    }

    // Fecha o modal quando o usuário pressiona Escape.
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

  return createPortal(
    <div className="modal-backdrop" onClick={onClose} role="presentation">
      <SurfaceCard
        as="div"
        className="modal-card"
        onClick={(event) => event.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descriptionId}
      >
        <div className="modal-card__header">
          <h2 className="modal-card__title" id={titleId}>
            {title}
          </h2>

          <button
            className="modal-card__close"
            type="button"
            onClick={onClose}
            aria-label="Fechar modal"
          >
            <CloseIcon />
          </button>
        </div>

        <div className="modal-card__description" id={descriptionId}>
          {description}
        </div>

        <div className="modal-card__actions">
          <Button variant="ghost" onClick={onClose}>
            {cancelLabel}
          </Button>
          <Button variant={confirmTone} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </div>
      </SurfaceCard>
    </div>,
    document.body
  );
}
