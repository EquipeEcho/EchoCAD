import {
  PropsWithChildren,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  AuthSession,
  AuthUser,
  LoginPayload,
  RegisterPayload,
  loginUser,
  registerUser,
} from "../services/api";

type AuthContextValue = {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isAuthLoading: boolean;
  login: (credentials: LoginPayload) => Promise<void>;
  register: (userData: RegisterPayload) => Promise<void>;
  logout: () => void;
};

const AUTH_USER_KEY = "echocad_auth_user";

const AuthContext = createContext<AuthContextValue | null>(null);

function readStoredSession(): AuthSession | null {
  const stored = window.localStorage.getItem(AUTH_USER_KEY);

  if (!stored) {
    console.log("No stored session found");
    return null;
  }

  try {
    const parsed = JSON.parse(stored);
    console.log("Stored session found:", { 
      has_access_token: !!parsed.access_token, 
      user_id: parsed.user?.id 
    });
    
    if (parsed && typeof parsed === "object" && "access_token" in parsed && "user" in parsed) {
      return parsed as AuthSession;
    }

    console.warn("Stored session format invalid");
    return null;
  } catch (e) {
    console.error("Error parsing stored session:", e);
    window.localStorage.removeItem(AUTH_USER_KEY);
    return null;
  }
}

export function AuthProvider({ children }: PropsWithChildren) {
  const [session, setSession] = useState<AuthSession | null>(() => readStoredSession());
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  const saveSession = (nextSession: AuthSession) => {
    console.log("Saving auth session:", { 
      user_id: nextSession.user?.id, 
      token_type: nextSession.token_type 
    });
    window.localStorage.setItem(AUTH_USER_KEY, JSON.stringify(nextSession));
    setSession(nextSession);
  };

  const clearSession = () => {
    console.log("Clearing auth session");
    window.localStorage.removeItem(AUTH_USER_KEY);
    setSession(null);
  };

  useEffect(() => {
    setIsAuthLoading(false);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: session?.user ?? null,
      isAuthenticated: Boolean(session?.user),
      isAuthLoading,
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
    [isAuthLoading, session],
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
