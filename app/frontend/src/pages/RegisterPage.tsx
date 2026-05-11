import { FormEvent, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { EyeIcon, EyeOffIcon, UserIcon } from "../components/Icons";
import { Logo } from "../components/Logo";
import { SurfaceCard } from "../components/SurfaceCard";
import { useAuth } from "../providers/AuthProvider";

export function RegisterPage() {
  const navigate = useNavigate();
  const { isAuthenticated, register } = useAuth();
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");

    if (password !== confirmPassword) {
      setErrorMessage("As senhas nao conferem.");
      return;
    }

    setIsSubmitting(true);

    try {
      await register({
        name,
        email,
        password,
        role: role.trim() || undefined,
      });
      navigate("/", { replace: true });
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Nao foi possivel cadastrar.");
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

          <nav className="auth-tabs" aria-label="Autenticacao">
            <Link className="auth-tabs__item" to="/login">Entrar</Link>
            <Link className="auth-tabs__item is-active" to="/cadastro" aria-current="page">Cadastro</Link>
          </nav>

          <div className="auth-card__header">
            <span className="auth-card__icon" aria-hidden="true">
              <UserIcon />
            </span>
            <div>
              <h1 className="auth-card__title">Cadastro</h1>
              <p className="auth-card__description">Crie uma conta para salvar projetos com seu usuario.</p>
            </div>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <label className="form-field">
              <span className="form-field__label">Nome</span>
              <input
                className="form-field__control"
                type="text"
                value={name}
                onChange={(event) => setName(event.target.value)}
                autoComplete="name"
                maxLength={100}
                required
              />
            </label>

            <label className="form-field">
              <span className="form-field__label">Cargo</span>
              <input
                className="form-field__control"
                type="text"
                value={role}
                onChange={(event) => setRole(event.target.value)}
                autoComplete="organization-title"
                maxLength={100}
              />
            </label>

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
                  autoComplete="new-password"
                  minLength={6}
                  maxLength={255}
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

            <label className="form-field">
              <span className="form-field__label">Confirmar senha</span>
              <span className="password-field">
                <input
                  className="form-field__control password-field__control"
                  type={isPasswordVisible ? "text" : "password"}
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  autoComplete="new-password"
                  minLength={6}
                  maxLength={255}
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
              {isSubmitting ? "Cadastrando..." : "Cadastrar"}
            </Button>
          </form>

        </SurfaceCard>
      </div>
    </main>
  );
}
