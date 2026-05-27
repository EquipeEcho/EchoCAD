import { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonVariant =
  | "primary"
  | "success"
  | "danger"
  | "secondary"
  | "ghost"
  | "icon"
  | "link";

type ButtonSize = "md" | "lg";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  size?: ButtonSize;
  leadingIcon?: ReactNode;
  trailingIcon?: ReactNode;
  fullWidth?: boolean;
};

// Padroniza botoes com variantes e tamanhos.
export function Button({
  children,
  className,
  variant = "primary",
  size = "md",
  leadingIcon,
  trailingIcon,
  fullWidth = false,
  type = "button",
  ...props
}: ButtonProps) {
  const classes = [
    "button",
    `button--${variant}`,
    `button--${size}`,
    fullWidth ? "button--full" : "",
    className || "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classes} type={type} {...props}>
      {leadingIcon ? <span className="button__icon">{leadingIcon}</span> : null}
      {children ? <span className="button__label">{children}</span> : null}
      {trailingIcon ? <span className="button__icon">{trailingIcon}</span> : null}
    </button>
  );
}
