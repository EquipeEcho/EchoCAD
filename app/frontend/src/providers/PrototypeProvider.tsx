import {
  PropsWithChildren,
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import {
  buildGeneratedDocumentFromUploads,
  buildHistoryDocumentFromGenerated,
  getFileKindFromName,
  mockHistoryDocuments,
} from "../data/mockData";
import {
  AddFilesResult,
  GeneratedDocument,
  HistoryDocument,
  ProjectSaveInput,
  ToastState,
  ToastTone,
  UploadDocument,
} from "../types/documents";
import { formatInputDate } from "../utils/date";

type ProcessingResult = {
  file_url: string;
};

type PrototypeContextValue = {
  uploadedFiles: UploadDocument[];
  historyDocuments: HistoryDocument[];
  currentDocument: GeneratedDocument | null;
  shouldPromptProjectSave: boolean;
  toast: ToastState | null;
  addUploadedFiles: (fileList: FileList | File[]) => AddFilesResult;
  removeUploadedFile: (documentId: string) => void;
  clearUploadedFiles: () => void;
  completeProcessing: (apiResults?: ProcessingResult[]) => GeneratedDocument | null;
  saveCurrentProject: (projectInfo: ProjectSaveInput) => void;
  openHistoryPreview: (documentId: string) => void;
  removeHistoryDocument: (documentId: string) => void;
  downloadHistoryBundle: () => void;
  simulatePreviewAction: (fileName: string) => void;
  downloadDocumentAsset: (url: string | undefined, label: string) => void;
  showToast: (message: string, tone?: ToastTone) => void;
};

const PrototypeContext = createContext<PrototypeContextValue | null>(null);

// Converte um arquivo válido para o formato usado no upload.
function buildUploadDocument(file: File): UploadDocument | null {
  const kind = getFileKindFromName(file.name);

  if (!kind) {
    return null;
  }

  return {
    id: `${file.name}-${file.size}-${file.lastModified}`,
    name: file.name,
    kind,
    file,
  };
}

// Centraliza o estado do protótipo e das simulações.
export function PrototypeProvider({ children }: PropsWithChildren) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadDocument[]>([]);
  const uploadedFilesRef = useRef<UploadDocument[]>([]);
  const [historyDocuments, setHistoryDocuments] =
    useState<HistoryDocument[]>(mockHistoryDocuments);
  const [currentDocument, setCurrentDocument] = useState<GeneratedDocument | null>(
    null
  );
  const [shouldPromptProjectSave, setShouldPromptProjectSave] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);

  useEffect(() => {
    if (!toast) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      setToast(null);
    }, 2600);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [toast]);

  // Exibe uma notificação temporária na interface.
  const showToast = (message: string, tone: ToastTone = "info") => {
    setToast({
      id: Date.now(),
      tone,
      message,
    });
  };

  // Mantém o estado e a referência de uploads sincronizados.
  const syncUploadedFiles = (nextFiles: UploadDocument[]) => {
    uploadedFilesRef.current = nextFiles;
    setUploadedFiles(nextFiles);
  };

  // Adiciona apenas arquivos válidos e não duplicados.
  const addUploadedFiles = (fileList: FileList | File[]): AddFilesResult => {
    const incomingFiles = Array.from(fileList);
    const parsedFiles = incomingFiles.map(buildUploadDocument);
    const currentFiles = uploadedFilesRef.current;
    const nextFiles = [...currentFiles];
    const knownIds = new Set(currentFiles.map((file) => file.id));
    let duplicateCount = 0;
    let invalidCount = 0;
    let addedCount = 0;

    parsedFiles.forEach((file) => {
      if (!file) {
        invalidCount += 1;
        return;
      }

      if (knownIds.has(file.id)) {
        duplicateCount += 1;
        return;
      }

      knownIds.add(file.id);
      nextFiles.push(file);
      addedCount += 1;
    });

    if (addedCount > 0) {
      syncUploadedFiles(nextFiles);
    }

    return { addedCount, duplicateCount, invalidCount };
  };

  // Remove um arquivo da lista de upload.
  const removeUploadedFile = (documentId: string) => {
    syncUploadedFiles(
      uploadedFilesRef.current.filter((document) => document.id !== documentId)
    );
  };

  // Limpa todos os arquivos pendentes de upload.
  const clearUploadedFiles = () => {
    syncUploadedFiles([]);
  };

  // Gera o documento final e deixa os dados do projeto para preenchimento.
  const completeProcessing = (apiResults: ProcessingResult[] = []) => {
    const filesToProcess = uploadedFilesRef.current;

    if (filesToProcess.length === 0) {
      return null;
    }

    const generatedDocument: GeneratedDocument = {
      ...buildGeneratedDocumentFromUploads(filesToProcess),
      file_urls: apiResults.map((result) => result.file_url),
    };

    setCurrentDocument(generatedDocument);
    setShouldPromptProjectSave(true);
    syncUploadedFiles([]);
    showToast("Processamento concluído com sucesso.", "success");

    return generatedDocument;
  };

  // Salva ou atualiza as informações do projeto no documento atual.
  const saveCurrentProject = (projectInput: ProjectSaveInput) => {
    if (!currentDocument) {
      showToast("Nenhum documento disponível para salvar.", "error");
      return;
    }

    const projectInfo = {
      name: projectInput.name.trim(),
      projectDate: projectInput.projectDate,
      responsible: projectInput.responsible.trim(),
      notes: projectInput.notes.trim(),
      savedAt: new Date().toISOString(),
    };
    const savedDocument: GeneratedDocument = {
      ...currentDocument,
      title: `Memorial de cálculo - ${projectInfo.name}`,
      createdAt: formatInputDate(projectInfo.projectDate),
      projectInfo,
    };
    const historyDocument = buildHistoryDocumentFromGenerated(savedDocument);

    setCurrentDocument(savedDocument);
    setShouldPromptProjectSave(false);
    setHistoryDocuments((currentHistory) => [
      historyDocument,
      ...currentHistory.filter(
        (document) => document.document.id !== savedDocument.id
      ),
    ]);
    showToast("Projeto salvo no histórico.", "success");
  };

  // Abre um documento do histórico na área de resultado.
  const openHistoryPreview = (documentId: string) => {
    const historyDocument = historyDocuments.find(
      (document) => document.id === documentId
    );

    if (!historyDocument) {
      showToast("Documento não encontrado.", "error");
      return;
    }

    setCurrentDocument(historyDocument.document);
    setShouldPromptProjectSave(false);
  };

  // Remove um item do histórico salvo.
  const removeHistoryDocument = (documentId: string) => {
    setHistoryDocuments((currentHistory) =>
      currentHistory.filter((document) => document.id !== documentId)
    );
    showToast("Documento removido do histórico.", "info");
  };

  // Simula o download de todos os itens do histórico.
  const downloadHistoryBundle = () => {
    if (historyDocuments.length === 0) {
      showToast("Não há documentos no histórico para download.", "error");
      return;
    }

    showToast("Pacote do histórico pronto para download.", "success");
  };

  // Simula a abertura de um arquivo para visualização.
  const simulatePreviewAction = (fileName: string) => {
    showToast(`Pré-visualização simulada: ${fileName}.`, "info");
  };

  // Baixa o arquivo gerado pelo backend.
  const downloadDocumentAsset = async (url: string | undefined, label: string) => {
    if (!url) {
      showToast("Arquivo indisponível para download.", "error");
      return;
    }

    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error("Erro ao baixar arquivo");
      }

      const blob = await response.blob();
      const objectUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = objectUrl;
      link.download = label.includes(".") ? label : `${label}.xlsx`;

      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(objectUrl);

      showToast(`Download de ${label} iniciado.`, "success");
    } catch (error) {
      console.error(error);
      showToast("Erro ao baixar o arquivo.", "error");
    }
  };

  return (
    <PrototypeContext.Provider
      value={{
        uploadedFiles,
        historyDocuments,
        currentDocument,
        shouldPromptProjectSave,
        toast,
        addUploadedFiles,
        removeUploadedFile,
        clearUploadedFiles,
        completeProcessing,
        saveCurrentProject,
        openHistoryPreview,
        removeHistoryDocument,
        downloadHistoryBundle,
        simulatePreviewAction,
        downloadDocumentAsset,
        showToast,
      }}
    >
      {children}
    </PrototypeContext.Provider>
  );
}

// Retorna o contexto principal do protótipo.
export function usePrototype() {
  const context = useContext(PrototypeContext);

  if (!context) {
    throw new Error("usePrototype must be used within PrototypeProvider.");
  }

  return context;
}
