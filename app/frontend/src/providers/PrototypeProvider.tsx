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
  ToastState,
  ToastTone,
  UploadDocument,
} from "../types/documents";

type PrototypeContextValue = {
  uploadedFiles: UploadDocument[];
  historyDocuments: HistoryDocument[];
  currentDocument: GeneratedDocument | null;
  toast: ToastState | null;
  addUploadedFiles: (fileList: FileList | File[]) => AddFilesResult;
  removeUploadedFile: (documentId: string) => void;
  clearUploadedFiles: () => void;
  completeProcessing: (apiResults: any[]) => GeneratedDocument | null;
  openHistoryPreview: (documentId: string) => void;
  removeHistoryDocument: (documentId: string) => void;
  downloadHistoryBundle: () => void;
  simulatePreviewAction: (fileName: string) => void;
  downloadDocumentAsset: (url: string, label: string) => void;
  showToast: (message: string, tone?: ToastTone) => void;
};

const PrototypeContext = createContext<PrototypeContextValue | null>(null);

// Converte um arquivo valido para o formato usado no upload.
function buildUploadDocument(file: File): UploadDocument | null {
  const kind = getFileKindFromName(file.name);

  if (!kind) {
    return null;
  }

  return {
    id: `${file.name}-${file.size}-${file.lastModified}`,
    name: file.name,
    kind,
    file: file
  };
}

// Centraliza o estado do prototipo e das simulacoes.
export function PrototypeProvider({ children }: PropsWithChildren) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadDocument[]>([]);
  const uploadedFilesRef = useRef<UploadDocument[]>([]);
  const [historyDocuments, setHistoryDocuments] =
    useState<HistoryDocument[]>(mockHistoryDocuments);
  const [currentDocument, setCurrentDocument] = useState<GeneratedDocument | null>(
    null
  );
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

  // Exibe uma notificacao temporaria na interface.
  const showToast = (message: string, tone: ToastTone = "info") => {
    setToast({
      id: Date.now(),
      tone,
      message,
    });
  };

  // Mantem o estado e a referencia de uploads sincronizados.
  const syncUploadedFiles = (nextFiles: UploadDocument[]) => {
    uploadedFilesRef.current = nextFiles;
    setUploadedFiles(nextFiles);
  };

  // Adiciona apenas arquivos validos e nao duplicados.
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

  // Gera o documento final e atualiza o historico.
  const completeProcessing = (apiResults: any[]) => {
    if (apiResults.length === 0) {
      return null;
    }

    const generatedDocument: GeneratedDocument = {
      id: Date.now().toString(),
      title: "Memorial de Cálculo",
      subtitle: "Gerado automaticamente",
      createdAt: new Date().toISOString(),
      reference: "REF-001",
      versionLabel: "v1.0",
      summary: "Documento gerado com sucesso.",

      previewLines: [],
      tableRows: [],
      sourceFiles: [],

      file_urls: apiResults.map((res) => res.file_url),
    };

    const historyDocument = buildHistoryDocumentFromGenerated(generatedDocument);

    setCurrentDocument(generatedDocument);
    setHistoryDocuments((currentHistory) => [historyDocument, ...currentHistory]);

    syncUploadedFiles([]);
    showToast("Processamento concluído com sucesso.", "success");

    return generatedDocument;
  };

  // Abre um documento do historico na area de resultado.
  const openHistoryPreview = (documentId: string) => {
    const historyDocument = historyDocuments.find(
      (document) => document.id === documentId
    );

    if (!historyDocument) {
      showToast("Documento não encontrado.", "error");
      return;
    }

    setCurrentDocument(historyDocument.document);
  };

  // Remove um item do historico salvo.
  const removeHistoryDocument = (documentId: string) => {
    setHistoryDocuments((currentHistory) =>
      currentHistory.filter((document) => document.id !== documentId)
    );
    showToast("Documento removido do histórico.", "info");
  };

  // Simula o download de todos os itens do historico.
  const downloadHistoryBundle = () => {
    if (historyDocuments.length === 0) {
      showToast("Não há documentos no histórico para download.", "error");
      return;
    }

    showToast("Pacote do histórico pronto para download.", "success");
  };

  // Simula a abertura de um arquivo para visualizacao.
  const simulatePreviewAction = (fileName: string) => {
    showToast(`Pré-visualização simulada: ${fileName}.`, "info");
  };

  // Simula o download de um arquivo gerado.
  const downloadDocumentAsset = async (url: string, label: string) => {
    try {
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error("Erro ao baixar arquivo");
      }

      const blob = await response.blob();

      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);

      // define nome do arquivo
      link.download = label.includes(".") ? label : `${label}.xlsx`;

      document.body.appendChild(link);
      link.click();
      link.remove();

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
        toast,
        addUploadedFiles,
        removeUploadedFile,
        clearUploadedFiles,
        completeProcessing,
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

// Retorna o contexto principal do prototipo.
export function usePrototype() {
  const context = useContext(PrototypeContext);

  if (!context) {
    throw new Error("usePrototype must be used within PrototypeProvider.");
  }

  return context;
}
