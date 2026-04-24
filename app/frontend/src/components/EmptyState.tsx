import { ReactNode } from "react";
import { Button } from "./Button";
import { SurfaceCard } from "./SurfaceCard";

type EmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: ReactNode;
  tone?: "neutral" | "error";
};

// Mostra uma mensagem quando não há conteúdo.
export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
  icon,
  tone = "neutral",
}: EmptyStateProps) {
  return (
    <SurfaceCard className={`empty-state empty-state--${tone}`}>
      {icon ? <div className="empty-state__icon">{icon}</div> : null}
      <h2 className="empty-state__title">{title}</h2>
      <p className="empty-state__description">{description}</p>
      {actionLabel && onAction ? (
        <Button variant={tone === "error" ? "primary" : "success"} onClick={onAction}>
          {actionLabel}
        </Button>
      ) : null}
    </SurfaceCard>
  );
}
