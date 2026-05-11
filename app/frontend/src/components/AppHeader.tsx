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
  const { theme, toggleTheme } = useTheme();
  const { isAIProcessing } = usePrototype();
  const { isAuthenticated, logout, user } = useAuth();
  const homeIsActive = !["/historico", "/normas", "/processando", "/resultado", "/login", "/cadastro"].includes(location.pathname);
  const isDarkMode = theme === "dark";

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="site-header">
      <div className="header-content">
        <Logo />

        <div className="header-actions">
          {isAuthenticated ? (
            <>
              <nav className="main-nav" aria-label="Navegacao principal">
                <NavLink className={`nav-link${homeIsActive ? " is-active" : ""}`} to="/">
                  Home
                </NavLink>
                <NavLink className={`nav-link${location.pathname === "/historico" ? " is-active" : ""}`} to="/historico">
                  Historico
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

              <div className="user-menu" aria-label="Usuario autenticado">
                <span className="user-menu__avatar" aria-hidden="true">
                  <UserIcon />
                </span>
                <span className="user-menu__name">{user?.name || "Usuario"}</span>
              </div>

              <Button
                aria-label="Sair da conta"
                className="header-icon-button"
                leadingIcon={<LogOutIcon />}
                onClick={handleLogout}
                title="Sair"
                variant="icon"
              />
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

          <Button
            aria-label={isDarkMode ? "Ativar modo claro" : "Ativar modo escuro"}
            aria-pressed={isDarkMode}
            className="theme-toggle"
            leadingIcon={isDarkMode ? <SunIcon /> : <MoonIcon />}
            onClick={toggleTheme}
            variant="secondary"
          >
            {isDarkMode ? "Modo claro" : "Modo escuro"}
          </Button>
        </div>
      </div>
    </header>
  );
}
