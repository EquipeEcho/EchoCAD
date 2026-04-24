import { NavLink, useLocation } from "react-router-dom";
import { useTheme } from "../providers/ThemeProvider";
import { Button } from "./Button";
import { MoonIcon, SunIcon } from "./Icons";
import { Logo } from "./Logo";

// Renderiza o cabeçalho principal e a navegação.
export function AppHeader() {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const homeIsActive = location.pathname !== "/historico";
  const isDarkMode = theme === "dark";

  return (
    <header className="site-header">
      <div className="header-content">
        <Logo />

        <div className="header-actions">
          <nav className="main-nav" aria-label={"Navega\u00E7\u00E3o principal"}>
            <NavLink
              className={`nav-link${homeIsActive ? " is-active" : ""}`}
              to="/"
            >
              Home
            </NavLink>
            <NavLink
              className={`nav-link${location.pathname === "/historico" ? " is-active" : ""}`}
              to="/historico"
            >
              {"Hist\u00F3rico"}
            </NavLink>
          </nav>

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
