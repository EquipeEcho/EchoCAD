import { usePrototype } from "../providers/PrototypeProvider";
import { InfoCircleIcon, ToastSuccessIcon } from "./Icons";

// Exibe a notificação ativa do sistema.
export function ToastMessage() {
  const { toast } = usePrototype();

  if (!toast) {
    return null;
  }

  return (
    <div className={`toast toast--${toast.tone}`} role="status" aria-live="polite">
      <span className="toast__icon" aria-hidden="true">
        {toast.tone === "success" ? <ToastSuccessIcon /> : <InfoCircleIcon />}
      </span>
      <span className="toast__message">{toast.message}</span>
    </div>
  );
}
