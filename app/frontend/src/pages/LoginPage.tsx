import { FormEvent, useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EyeIcon, EyeOffIcon, LockIcon } from "../components/Icons";
import { Logo } from "../components/Logo";
import { SurfaceCard } from "../components/SurfaceCard";
import { useAuth } from "../providers/AuthProvider";

type LocationState = {
  from?: {
    pathname?: string;
  };
};

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fromPath = (location.state as LocationState | null)?.from?.pathname || "/";

  if (isAuthenticated) {
    return <Navigate to={fromPath} replace />;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      console.log("Attempting login with:", { email, password: "***" });
      await login({ email, password });
      console.log("Login successful, stored session:", window.localStorage.getItem("echocad_auth_user"));
      navigate(fromPath, { replace: true });
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : "Não foi possível entrar.";
      console.error("Login error:", errorMsg);
      setErrorMessage(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="page auth-page">
      <div className="auth-page__content">
        <SurfaceCard className="auth-card">
          <div className="auth-card__brand">
            <Logo subtle />
          </div>

          <nav className="auth-tabs" aria-label="Autenticação">
            <Link className="auth-tabs__item is-active" to="/login" aria-current="page">Entrar</Link>
            <Link className="auth-tabs__item" to="/cadastro">Cadastro</Link>
          </nav>

          <div className="auth-card__header">
            <span className="auth-card__icon" aria-hidden="true">
              <LockIcon />
            </span>
            <div>
              <h1 className="auth-card__title">Entrar</h1>
              <p className="auth-card__description">Acesse sua conta para continuar no EchoCAD.</p>
            </div>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <label className="form-field">
              <span className="form-field__label">E-mail</span>
              <input
                className="form-field__control"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="email"
                required
              />
            </label>

            <label className="form-field">
              <span className="form-field__label">Senha</span>
              <span className="password-field">
                <input
                  className="form-field__control password-field__control"
                  type={isPasswordVisible ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  autoComplete="current-password"
                  required
                />
                <button
                  className="password-field__toggle"
                  type="button"
                  onClick={() => setIsPasswordVisible((current) => !current)}
                  aria-label={isPasswordVisible ? "Ocultar senha" : "Mostrar senha"}
                  title={isPasswordVisible ? "Ocultar senha" : "Mostrar senha"}
                >
                  {isPasswordVisible ? <EyeOffIcon /> : <EyeIcon />}
                </button>
              </span>
            </label>

            {errorMessage ? (
              <p className="auth-form__message auth-form__message--error" role="alert">
                {errorMessage}
              </p>
            ) : null}

            <Button fullWidth type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Entrando..." : "Entrar"}
            </Button>
          </form>

        </SurfaceCard>
      </div>
    </main>
  );
}
