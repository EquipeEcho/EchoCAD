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

type FileRowProps = {
  name: string;
  kind: FileKind;
  date?: string;
  size?: string;
  actions: FileAction[];
  variant?: "upload" | "history";
};

// Exibe uma linha com dados e ações de um arquivo.
export function FileRow({
  name,
  kind,
  date,
  size,
  actions,
  variant = "upload",
}: FileRowProps) {
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
            <span className="file-row__kind">{kind.toUpperCase()}</span>
            <span className="file-row__hint">
              {variant === "history"
                ? "Projeto salvo"
                : "Pronto para processamento"}
            </span>
          </div>
        </div>
      </div>

      {variant === "history" ? (
        <>
          <div className="file-row__meta-block">
            <span className="file-row__meta-label">Data</span>
            <p className="file-row__meta">{date}</p>
          </div>
          <div className="file-row__meta-block">
            <span className="file-row__meta-label">Tamanho</span>
            <p className="file-row__meta">{size}</p>
          </div>
        </>
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
