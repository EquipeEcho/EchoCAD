import { FormEvent, useEffect, useRef, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../providers/AuthProvider";
import { usePrototype } from "../hooks/usePrototype";
import { useTheme } from "../providers/ThemeProvider";
import {
  GroqApiKeyStatus,
  changePassword,
  getGroqApiKeyStatus,
  removeGroqApiKey,
  saveGroqApiKey,
} from "../services/api";
import { Button } from "./Button";
import { LogOutIcon, MoonIcon, SpinnerIcon, SunIcon, UserIcon } from "./Icons";
import { Logo } from "./Logo";

type UserPanel = "password" | "groq" | null;

export function AppHeader() {
  const location = useLocation();
  const navigate = useNavigate();
  const userMenuRef = useRef<HTMLDivElement>(null);
  const { theme, toggleTheme } = useTheme();
  const { isAIProcessing } = usePrototype();
  const { isAuthenticated, logout, user } = useAuth();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const [activeUserPanel, setActiveUserPanel] = useState<UserPanel>(null);
  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [groqKeyInput, setGroqKeyInput] = useState("");
  const [groqStatus, setGroqStatus] = useState<GroqApiKeyStatus | null>(null);
  const [userSettingsMessage, setUserSettingsMessage] = useState<string | null>(null);
  const [isSavingUserSettings, setIsSavingUserSettings] = useState(false);
  const homeIsActive = !["/historico", "/normas", "/processando", "/resultado", "/login", "/cadastro"].includes(location.pathname);
  const isDarkMode = theme === "dark";

  const handleLogout = () => {
    setIsUserMenuOpen(false);
    logout();
    navigate("/login", { replace: true });
  };

  useEffect(() => {
    setIsUserMenuOpen(false);
    setActiveUserPanel(null);
    setUserSettingsMessage(null);
  }, [location.pathname]);

  useEffect(() => {
    if (!userSettingsMessage) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      setUserSettingsMessage(null);
    }, 3500);

    return () => window.clearTimeout(timeoutId);
  }, [userSettingsMessage]);

  useEffect(() => {
    if (!isUserMenuOpen || !isAuthenticated) {
      return;
    }

    let isMounted = true;
    getGroqApiKeyStatus()
      .then((status) => {
        if (isMounted) {
          setGroqStatus(status);
        }
      })
      .catch(() => {
        if (isMounted) {
          setGroqStatus(null);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [isAuthenticated, isUserMenuOpen]);

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

  const handlePasswordSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setUserSettingsMessage("A confirmação precisa ser igual à nova senha.");
      return;
    }

    setIsSavingUserSettings(true);
    setUserSettingsMessage(null);
    try {
      await changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });
      setPasswordForm({
        current_password: "",
        new_password: "",
        confirm_password: "",
      });
      setUserSettingsMessage("Senha alterada com sucesso.");
    } catch (error) {
      setUserSettingsMessage(
        error instanceof Error ? error.message : "Não foi possível alterar a senha.",
      );
    } finally {
      setIsSavingUserSettings(false);
    }
  };

  const handleGroqSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!groqKeyInput.trim()) {
      setUserSettingsMessage("Informe uma chave Groq válida.");
      return;
    }

    setIsSavingUserSettings(true);
    setUserSettingsMessage(null);
    try {
      const status = await saveGroqApiKey(groqKeyInput.trim());
      setGroqStatus(status);
      setGroqKeyInput("");
      setUserSettingsMessage("Chave Groq salva com sucesso.");
    } catch (error) {
      setUserSettingsMessage(
        error instanceof Error ? error.message : "Não foi possível salvar a chave Groq.",
      );
    } finally {
      setIsSavingUserSettings(false);
    }
  };

  const handleRemoveGroqKey = async () => {
    setIsSavingUserSettings(true);
    setUserSettingsMessage(null);
    try {
      const status = await removeGroqApiKey();
      setGroqStatus(status);
      setGroqKeyInput("");
      setUserSettingsMessage("Chave Groq removida.");
    } catch (error) {
      setUserSettingsMessage(
        error instanceof Error ? error.message : "Não foi possível remover a chave Groq.",
      );
    } finally {
      setIsSavingUserSettings(false);
    }
  };

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
                        {user?.role ? (
                          <span className="user-popover__role">{user.role}</span>
                        ) : null}
                      </div>
                    </div>

                    <dl className="user-popover__details">
                      <div>
                        <dt>Groq</dt>
                        <dd>
                          <span
                            className={`user-popover__status${
                              groqStatus?.configured ? " is-configured" : ""
                            }`}
                          >
                            {groqStatus?.configured ? groqStatus.masked_key : "Nao configurada"}
                          </span>
                        </dd>
                      </div>
                    </dl>

                    <div className="user-popover__settings">
                      <p className="user-popover__section-label">Conta</p>
                      <div className="user-popover__quick-actions" role="tablist" aria-label="Configurações da conta">
                        <button
                          className={`user-settings-tab${activeUserPanel === "password" ? " is-active" : ""}`}
                          aria-selected={activeUserPanel === "password"}
                          onClick={() =>
                            setActiveUserPanel((current) =>
                              current === "password" ? null : "password",
                            )
                          }
                          role="tab"
                          type="button"
                        >
                          Alterar senha
                        </button>
                        <button
                          className={`user-settings-tab${activeUserPanel === "groq" ? " is-active" : ""}`}
                          aria-selected={activeUserPanel === "groq"}
                          onClick={() =>
                            setActiveUserPanel((current) =>
                              current === "groq" ? null : "groq",
                            )
                          }
                          role="tab"
                          type="button"
                        >
                          Chave Groq
                        </button>
                      </div>

                      {activeUserPanel === "password" ? (
                        <form className="user-settings-form" onSubmit={handlePasswordSubmit}>
                          <label className="form-field">
                            <span className="form-field__label">Senha atual</span>
                            <input
                              className="form-field__control"
                              minLength={6}
                              onChange={(event) =>
                                setPasswordForm((current) => ({
                                  ...current,
                                  current_password: event.target.value,
                                }))
                              }
                              required
                              type="password"
                              value={passwordForm.current_password}
                            />
                          </label>
                          <label className="form-field">
                            <span className="form-field__label">Nova senha</span>
                            <input
                              className="form-field__control"
                              minLength={6}
                              onChange={(event) =>
                                setPasswordForm((current) => ({
                                  ...current,
                                  new_password: event.target.value,
                                }))
                              }
                              required
                              type="password"
                              value={passwordForm.new_password}
                            />
                          </label>
                          <label className="form-field">
                            <span className="form-field__label">Confirmar nova senha</span>
                            <input
                              className="form-field__control"
                              minLength={6}
                              onChange={(event) =>
                                setPasswordForm((current) => ({
                                  ...current,
                                  confirm_password: event.target.value,
                                }))
                              }
                              required
                              type="password"
                              value={passwordForm.confirm_password}
                            />
                          </label>
                          <Button
                            disabled={isSavingUserSettings}
                            leadingIcon={
                              isSavingUserSettings ? <SpinnerIcon className="spin" /> : undefined
                            }
                            type="submit"
                            variant="primary"
                          >
                            Salvar senha
                          </Button>
                        </form>
                      ) : null}

                      {activeUserPanel === "groq" ? (
                        <form className="user-settings-form" onSubmit={handleGroqSubmit}>
                          <label className="form-field">
                            <span className="form-field__label">Chave da API Groq</span>
                            <input
                              autoComplete="off"
                              className="form-field__control"
                              onChange={(event) => setGroqKeyInput(event.target.value)}
                              placeholder="gsk_..."
                              type="password"
                              value={groqKeyInput}
                            />
                          </label>
                          <div className="user-settings-form__actions">
                            <Button
                              disabled={isSavingUserSettings}
                              leadingIcon={
                                isSavingUserSettings ? <SpinnerIcon className="spin" /> : undefined
                              }
                              type="submit"
                              variant="primary"
                            >
                              Salvar chave
                            </Button>
                            {groqStatus?.configured ? (
                              <Button
                                disabled={isSavingUserSettings}
                                onClick={handleRemoveGroqKey}
                                variant="ghost"
                              >
                                Remover chave
                              </Button>
                            ) : null}
                          </div>
                        </form>
                      ) : null}

                      {userSettingsMessage ? (
                        <p className="user-settings-message" role="status">
                          {userSettingsMessage}
                        </p>
                      ) : null}
                    </div>

                    <Button
                      fullWidth
                      className="user-popover__logout"
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
