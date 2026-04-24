import { ReactNode } from "react";

type SectionTitleProps = {
  eyebrow?: string;
  title: string;
  titleId?: string;
  description?: string;
  actions?: ReactNode;
  align?: "left" | "center";
  className?: string;
};

// Exibe título, descrição e ações de uma seção.
export function SectionTitle({
  eyebrow,
  title,
  titleId,
  description,
  actions,
  align = "left",
  className,
}: SectionTitleProps) {
  const classes = [
    "section-title",
    `section-title--${align}`,
    className ?? "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={classes}>
      <div className="section-title__content">
        {eyebrow ? <p className="section-heading__eyebrow">{eyebrow}</p> : null}
        <h1 className="section-title__heading" id={titleId}>
          {title}
        </h1>
        {description ? (
          <p className="section-title__description">{description}</p>
        ) : null}
      </div>

      {actions ? <div className="section-title__actions">{actions}</div> : null}
    </div>
  );
}
