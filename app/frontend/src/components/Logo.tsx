import { Link } from "react-router-dom";
import { EchoCadIcon } from "./Icons";

type LogoProps = {
  to?: string;
  subtle?: boolean;
};

// Renderiza a marca com link para navegação.
export function Logo({ to = "/", subtle = false }: LogoProps) {
  return (
    <Link
      aria-label="EchoCAD, ir para a página inicial"
      className={`brand${subtle ? " brand--subtle" : ""}`}
      to={to}
    >
      <span className="brand-mark" aria-hidden="true">
        <EchoCadIcon />
      </span>
      <span className="brand-text">EchoCAD</span>
    </Link>
  );
}
