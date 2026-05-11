import {
  PropsWithChildren,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
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

function readStoredUser() {
  const storedUser = window.localStorage.getItem(AUTH_USER_KEY);

  if (!storedUser) {
    return null;
  }

  try {
    return JSON.parse(storedUser) as AuthUser;
  } catch {
    window.localStorage.removeItem(AUTH_USER_KEY);
    return null;
  }
}

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<AuthUser | null>(() => readStoredUser());
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  const saveSession = (nextUser: AuthUser) => {
    window.localStorage.setItem(AUTH_USER_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
  };

  const clearSession = () => {
    window.localStorage.removeItem(AUTH_USER_KEY);
    setUser(null);
  };

  useEffect(() => {
    setIsAuthLoading(false);
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isAuthLoading,
      login: async (credentials) => {
        const response = await loginUser(credentials);
        saveSession(response.user);
      },
      register: async (userData) => {
        const response = await registerUser(userData);
        saveSession(response.user);
      },
      logout: clearSession,
    }),
    [isAuthLoading, user],
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
