import { ReactNode } from "react";
import { FileKind } from "../types/documents";
import { IconAction } from "./IconAction";
import { FileTypeIcon } from "./Icons";

type FileAction = {
  label: string;
  icon: ReactNode;
  onClick: () => void;
  tone?: "neutral" | "danger";
};

type FileRowMeta = {
  label: string;
  value: string;
};

type FileRowProps = {
  name: string;
  kind: FileKind;
  date?: string;
  size?: string;
  hint?: string;
  metaItems?: FileRowMeta[];
  statusControl?: ReactNode;
  actions: FileAction[];
  variant?: "upload" | "history" | "standard";
};

// Exibe uma linha com dados e ações de um arquivo.
function getKindLabel(kind: FileKind) {
  return kind === "project" ? "PROJ" : kind.toUpperCase();
}

export function FileRow({
  name,
  kind,
  date,
  size,
  hint,
  metaItems,
  statusControl,
  actions,
  variant = "upload",
}: FileRowProps) {
  const resolvedHint =
    hint ??
    (variant === "history"
      ? "Projeto salvo"
      : variant === "standard"
        ? "Norma técnica"
        : "Pronto para processamento");
  const resolvedMetaItems =
    metaItems ??
    (variant === "history"
      ? [
          { label: "Data", value: date || "-" },
          { label: "Tamanho", value: size || "-" },
        ]
      : []);

  return (
    <div
      className={`file-row file-row--${variant}`}
      data-kind={kind}
      role="listitem"
    >
      <div className="file-row__main">
        <span className="file-row__icon" aria-hidden="true">
          <FileTypeIcon kind={kind} />
        </span>
        <div className="file-row__content">
          <p className="file-row__name">{name}</p>
          <div className="file-row__subline">
            <span className="file-row__kind">{getKindLabel(kind)}</span>
            <span className="file-row__hint">{resolvedHint}</span>
          </div>
        </div>
      </div>

      {resolvedMetaItems.length > 0 ? (
        resolvedMetaItems.map((item) => (
          <div className="file-row__meta-block" key={item.label}>
            <span className="file-row__meta-label">{item.label}</span>
            <p className="file-row__meta">{item.value}</p>
          </div>
        ))
      ) : null}

      {statusControl ? (
        <div className="file-row__control">{statusControl}</div>
      ) : null}

      <div className="file-row__actions">
        {actions.map((action) => (
          <IconAction
            key={action.label}
            label={action.label}
            icon={action.icon}
            onClick={action.onClick}
            tone={action.tone}
          />
        ))}
      </div>
    </div>
  );
}
