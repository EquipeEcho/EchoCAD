import { ReactNode } from "react";
import { Button } from "./Button";

type IconActionProps = {
  label: string;
  icon: ReactNode;
  onClick: () => void;
  tone?: "neutral" | "danger";
};

// Renderiza uma ação compacta com ícone.
export function IconAction({
  label,
  icon,
  onClick,
  tone = "neutral",
}: IconActionProps) {
  return (
    <Button
      aria-label={label}
      className={`file-row__action${tone === "danger" ? " file-row__action--danger" : ""}`}
      variant="icon"
      onClick={onClick}
      type="button"
    >
      {icon}
    </Button>
  );
}
