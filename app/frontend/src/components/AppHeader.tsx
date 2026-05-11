import { useEffect, useRef, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../providers/AuthProvider";
import { usePrototype } from "../providers/PrototypeProvider";
import { useTheme } from "../providers/ThemeProvider";
import { Button } from "./Button";
import { LogOutIcon, MoonIcon, SpinnerIcon, SunIcon, UserIcon } from "./Icons";
import { Logo } from "./Logo";

export function AppHeader() {
  const location = useLocation();
  const navigate = useNavigate();
  const userMenuRef = useRef<HTMLDivElement>(null);
  const { theme, toggleTheme } = useTheme();
  const { isAIProcessing } = usePrototype();
  const { isAuthenticated, logout, user } = useAuth();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const homeIsActive = !["/historico", "/normas", "/processando", "/resultado", "/login", "/cadastro"].includes(location.pathname);
  const isDarkMode = theme === "dark";

  const handleLogout = () => {
    setIsUserMenuOpen(false);
    logout();
    navigate("/login", { replace: true });
  };

  useEffect(() => {
    setIsUserMenuOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!isUserMenuOpen) {
      return;
    }

    const handlePointerDown = (event: PointerEvent) => {
      if (!userMenuRef.current?.contains(event.target as Node)) {
        setIsUserMenuOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsUserMenuOpen(false);
      }
    };

    document.addEventListener("pointerdown", handlePointerDown);
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("pointerdown", handlePointerDown);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isUserMenuOpen]);

  return (
    <header className="site-header">
      <div className="header-content">
        <Logo />

        <div className="header-actions">
          {isAuthenticated ? (
            <>
              <nav className="main-nav" aria-label="Navegação principal">
                <NavLink className={`nav-link${homeIsActive ? " is-active" : ""}`} to="/">
                  Home
                </NavLink>
                <NavLink className={`nav-link${location.pathname === "/historico" ? " is-active" : ""}`} to="/historico">
                  Histórico
                </NavLink>
                <NavLink className={`nav-link${location.pathname === "/normas" ? " is-active" : ""}`} to="/normas">
                  Normas
                </NavLink>

                {isAIProcessing && (
                  <NavLink
                    className={`nav-link nav-link--active-processing${location.pathname === "/processando" ? " is-active" : ""}`}
                    to="/processando"
                  >
                    <SpinnerIcon />
                    <span>Processando...</span>
                  </NavLink>
                )}
              </nav>

              <Button
                aria-label={isDarkMode ? "Ativar modo claro" : "Ativar modo escuro"}
                aria-pressed={isDarkMode}
                className="header-icon-button"
                leadingIcon={isDarkMode ? <SunIcon /> : <MoonIcon />}
                onClick={toggleTheme}
                title={isDarkMode ? "Modo claro" : "Modo escuro"}
                variant="icon"
              />

              <div className="user-menu" ref={userMenuRef}>
                <Button
                  aria-expanded={isUserMenuOpen}
                  aria-haspopup="dialog"
                  aria-label="Abrir informações do usuário"
                  className="header-icon-button user-menu__trigger"
                  leadingIcon={<UserIcon />}
                  onClick={() => setIsUserMenuOpen((current) => !current)}
                  title="Usuário"
                  variant="icon"
                />

                {isUserMenuOpen ? (
                  <div className="user-popover" role="dialog" aria-label="Informações do usuário">
                    <div className="user-popover__header">
                      <span className="user-popover__avatar" aria-hidden="true">
                        <UserIcon />
                      </span>
                      <div className="user-popover__identity">
                        <strong>{user?.name || "Usuário"}</strong>
                        <span>{user?.email || "E-mail não informado"}</span>
                      </div>
                    </div>

                    <dl className="user-popover__details">
                      <div>
                        <dt>Cargo</dt>
                        <dd>{user?.role || "Não informado"}</dd>
                      </div>
                    </dl>

                    <Button
                      fullWidth
                      leadingIcon={<LogOutIcon />}
                      onClick={handleLogout}
                      variant="secondary"
                    >
                      Sair
                    </Button>
                  </div>
                ) : null}
              </div>
            </>
          ) : (
            <nav className="auth-nav" aria-label="Acesso">
              <NavLink className={`nav-link${location.pathname === "/login" ? " is-active" : ""}`} to="/login">
                Entrar
              </NavLink>
              <NavLink className={`nav-link nav-link--primary${location.pathname === "/cadastro" ? " is-active" : ""}`} to="/cadastro">
                Cadastro
              </NavLink>
            </nav>
          )}

          {!isAuthenticated ? (
            <Button
              aria-label={isDarkMode ? "Ativar modo claro" : "Ativar modo escuro"}
              aria-pressed={isDarkMode}
              className="header-icon-button"
              leadingIcon={isDarkMode ? <SunIcon /> : <MoonIcon />}
              onClick={toggleTheme}
              title={isDarkMode ? "Modo claro" : "Modo escuro"}
              variant="icon"
            />
          ) : null}
        </div>
      </div>
    </header>
  );
}
