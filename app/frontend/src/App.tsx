import { Navigate, Route, Routes } from "react-router-dom";
import { AppHeader } from "./components/AppHeader";
import { ToastMessage } from "./components/ToastMessage";
import { HistoryPage } from "./pages/HistoryPage";
import { HomePage } from "./pages/HomePage";
import { ProcessingPage } from "./pages/ProcessingPage";
import { ResultPage } from "./pages/ResultPage";

// Define as rotas principais da aplicação.
export default function App() {
  return (
    <div className="app-shell">
      <AppHeader />
      <ToastMessage />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/processando" element={<ProcessingPage />} />
        <Route path="/resultado" element={<ResultPage />} />
        <Route path="/historico" element={<HistoryPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
