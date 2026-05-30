import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { AppHeader } from "./components/AppHeader";
import { ToastMessage } from "./components/ToastMessage";
import { HistoryPage } from "./pages/HistoryPage";
import { HomePage } from "./pages/HomePage";
import { LoginPage } from "./pages/LoginPage";
import { ProcessingPage } from "./pages/ProcessingPage";
import { RegisterPage } from "./pages/RegisterPage";
import { ResultPage } from "./pages/ResultPage";
import { StandardsPage } from "./pages/StandardsPage";
import { useAuth } from "./providers/AuthProvider";

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const location = useLocation();
  const { isAuthenticated, isAuthLoading } = useAuth();

  if (isAuthLoading) {
    return (
      <main className="page">
        <div className="page__content page__content--narrow">
          <p className="status-note" role="status">Carregando sessão...</p>
        </div>
      </main>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default function App() {
  return (
    <>
      <AppHeader />
      <ToastMessage />

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/cadastro" element={<RegisterPage />} />
        <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
        <Route path="/processando" element={<ProtectedRoute><ProcessingPage /></ProtectedRoute>} />
        <Route path="/resultado" element={<ProtectedRoute><ResultPage /></ProtectedRoute>} />
        <Route path="/historico" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
        <Route path="/normas" element={<ProtectedRoute><StandardsPage /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
