import {
  PropsWithChildren,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  AUTH_SESSION_KEY,
  AuthSession,
  AuthUser,
  LoginPayload,
  RegisterPayload,
  SESSION_EXPIRED_EVENT,
  SESSION_EXPIRED_MESSAGE,
  clearStoredAuthSession,
  getSessionExpirationTime,
  isAuthSessionExpired,
  loginUser,
  readStoredAuthSession,
  registerUser,
} from "../services/api";

type AuthContextValue = {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isAuthLoading: boolean;
  authNotice: string | null;
  clearAuthNotice: () => void;
  login: (credentials: LoginPayload) => Promise<void>;
  register: (userData: RegisterPayload) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

function readInitialAuthState(): {
  session: AuthSession | null;
  notice: string | null;
} {
  const storedSession = readStoredAuthSession();

  if (isAuthSessionExpired(storedSession)) {
    clearStoredAuthSession();
    return {
      session: null,
      notice: SESSION_EXPIRED_MESSAGE,
    };
  }

  return {
    session: storedSession,
    notice: null,
  };
}

export function AuthProvider({ children }: PropsWithChildren) {
  const [initialAuthState] = useState<ReturnType<typeof readInitialAuthState>>(
    () => readInitialAuthState(),
  );
  const [session, setSession] = useState<AuthSession | null>(
    initialAuthState.session,
  );
  const [authNotice, setAuthNotice] = useState<string | null>(
    initialAuthState.notice,
  );
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  const saveSession = (nextSession: AuthSession) => {
    window.localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(nextSession));
    setSession(nextSession);
    setAuthNotice(null);
  };

  const clearSession = useCallback(() => {
    clearStoredAuthSession();
    setSession(null);
    setAuthNotice(null);
  }, []);

  const expireSession = useCallback((message = SESSION_EXPIRED_MESSAGE) => {
    clearStoredAuthSession();
    setSession(null);
    setAuthNotice(message);
  }, []);

  useEffect(() => {
    setIsAuthLoading(false);
  }, []);

  useEffect(() => {
    const handleSessionExpired = (event: Event) => {
      const sessionEvent = event as CustomEvent<{ message?: string }>;
      expireSession(sessionEvent.detail?.message);
    };

    window.addEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);

    return () => {
      window.removeEventListener(SESSION_EXPIRED_EVENT, handleSessionExpired);
    };
  }, [expireSession]);

  useEffect(() => {
    if (!session) {
      return;
    }

    const expiresAt = getSessionExpirationTime(session);

    if (!expiresAt) {
      return;
    }

    const millisecondsUntilExpiration = expiresAt - Date.now();

    if (millisecondsUntilExpiration <= 0) {
      expireSession();
      return;
    }

    const timeoutId = window.setTimeout(
      () => expireSession(),
      millisecondsUntilExpiration,
    );

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [expireSession, session]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: session?.user ?? null,
      isAuthenticated: Boolean(session?.user),
      isAuthLoading,
      authNotice,
      clearAuthNotice: () => setAuthNotice(null),
      login: async (credentials) => {
        const response = await loginUser(credentials);
        saveSession(response);
      },
      register: async (userData) => {
        const response = await registerUser(userData);
        saveSession(response);
      },
      logout: clearSession,
    }),
    [authNotice, clearSession, isAuthLoading, session],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider.");
  }

  return context;
}
