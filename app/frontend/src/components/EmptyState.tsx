import { ReactNode } from "react";
import { Button } from "./Button";

type EmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: ReactNode;
  tone?: "neutral" | "error";
  framed?: boolean;
  className?: string;
};

// Mostra uma mensagem quando não há conteúdo.
export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
  icon,
  tone = "neutral",
  framed = true,
  className,
}: EmptyStateProps) {
  const classes = [
    framed ? "surface-card" : "",
    "empty-state",
    `empty-state--${tone}`,
    className || "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={classes}>
      {icon ? <div className="empty-state__icon">{icon}</div> : null}
      <h2 className="empty-state__title">{title}</h2>
      <p className="empty-state__description">{description}</p>
      {actionLabel && onAction ? (
        <Button variant={tone === "error" ? "primary" : "success"} onClick={onAction}>
          {actionLabel}
        </Button>
      ) : null}
    </div>
  );
}
