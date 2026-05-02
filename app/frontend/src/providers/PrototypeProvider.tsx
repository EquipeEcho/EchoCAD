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
  mockTechnicalStandards,
} from "../data/mockData";
import {
  AddFilesResult,
  GeneratedDocument,
  HistoryDocument,
  ProjectInfo,
  ProjectSaveInput,
  TechnicalStandard,
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
  technicalStandards: TechnicalStandard[];
  isLoadingHistory: boolean;
  historyError: string | null;
  currentDocument: GeneratedDocument | null;
  shouldPromptProjectSave: boolean;
  toast: ToastState | null;
  addUploadedFiles: (fileList: FileList | File[]) => AddFilesResult;
  removeUploadedFile: (documentId: string) => void;
  clearUploadedFiles: () => void;
  completeProcessing: (
    apiResults?: ProcessingResult[],
    projectInfo?: ProjectSaveInput,
    sourceFiles?: UploadDocument[],
  ) => GeneratedDocument | null;
  saveCurrentProject: (projectInfo: ProjectSaveInput) => void;
  openHistoryPreview: (documentId: string) => void;
  removeHistoryDocument: (documentId: string) => void;
  downloadHistoryBundle: () => void;
  addTechnicalStandards: (fileList: FileList | File[]) => AddFilesResult;
  toggleStandard: (standardId: string) => void;
  downloadStandard: (standardId: string) => void;
  simulatePreviewAction: (fileName: string) => void;
  downloadDocumentAsset: (url: string | undefined, label: string) => void;
  showToast: (message: string, tone?: ToastTone) => void;
};

const PrototypeContext = createContext<PrototypeContextValue | null>(null);
const LIST_PROJETOS_URL = "http://127.0.0.1:8000/projeto/";

type ProjetoApiItem = {
  id?: number | string;
  nome?: string;
  descricao?: string | null;
  cliente?: string | null;
  data_criacao?: string | null;
};

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

function buildProjectInfo(projectInput: ProjectSaveInput): ProjectInfo {
  return {
    name: projectInput.name.trim(),
    cliente: projectInput.cliente?.trim(),
    descricao: projectInput.descricao?.trim(),
    savedAt: new Date().toISOString(),
  };
}

function formatFileSize(file: File) {
  if (file.size < 1024 * 1024) {
    return `${Math.max(1, Math.round(file.size / 1024))} KB`;
  }

  return `${(file.size / (1024 * 1024)).toFixed(1)} MB`;
}

function buildTechnicalStandard(file: File): TechnicalStandard | null {
  const kind = getFileKindFromName(file.name);

  if (kind !== "pdf") {
    return null;
  }

  const nameWithoutExtension = file.name.replace(/\.[^.]+$/, "");
  const codeMatch = nameWithoutExtension.match(/NBR\s*\d+/i);
  const code = codeMatch
    ? codeMatch[0].toUpperCase().replace(/\s+/, " ")
    : "Norma";

  return {
    id: `standard-${file.name}-${file.size}-${file.lastModified}`,
    name: nameWithoutExtension,
    code,
    category: "Personalizada",
    date: String(new Date(file.lastModified).getFullYear()),
    size: formatFileSize(file),
    kind,
    enabled: true,
    file,
  };
}

// Centraliza o estado do protótipo e das simulações.
export function PrototypeProvider({ children }: PropsWithChildren) {
  const [uploadedFiles, setUploadedFiles] = useState<UploadDocument[]>([]);
  const uploadedFilesRef = useRef<UploadDocument[]>([]);
  const [historyDocuments, setHistoryDocuments] = useState<HistoryDocument[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [technicalStandards, setTechnicalStandards] = useState<TechnicalStandard[]>(
    mockTechnicalStandards,
  );
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

  useEffect(() => {
    const fetchProjetos = async () => {
      setIsLoadingHistory(true);
      setHistoryError(null);

      try {
        const response = await fetch(LIST_PROJETOS_URL);
        if (!response.ok) {
          throw new Error(`Erro ao buscar projetos: ${response.status}`);
        }

        const projetos = (await response.json()) as ProjetoApiItem[];
        const normalizedHistory = projetos.map((projeto) => {
          const projectId = String(projeto.id ?? `projeto-${Math.random()}`);
          const createdAt = projeto.data_criacao
            ? new Date(projeto.data_criacao)
            : new Date();
          const previewLines = [
            projeto.descricao?.trim() || "Sem descrição informada.",
            `Cliente: ${projeto.cliente?.trim() || "Não informado"}`,
          ];

          return {
            id: projectId,
            name: projeto.nome?.trim() || `Projeto ${projectId}`,
            kind: "pdf" as const,
            date: createdAt.toLocaleDateString("pt-BR"),
            size: "N/A",
            document: {
              id: projectId,
              title: projeto.nome?.trim() || `Projeto ${projectId}`,
              subtitle: "Projeto cadastrado no banco de dados",
              createdAt: createdAt.toLocaleString("pt-BR"),
              reference: `PROJ-${projectId}`,
              versionLabel: "v1",
              summary: projeto.descricao?.trim() || "Projeto sem descrição.",
              previewLines,
              tableRows: [
                { label: "Cliente", value: projeto.cliente?.trim() || "Não informado" },
                { label: "ID do projeto", value: projectId },
              ],
              sourceFiles: [],
              file_urls: [],
            },
          };
        });

        setHistoryDocuments(normalizedHistory);
      } catch (error) {
        console.error(error);
        setHistoryError("Não foi possível carregar os projetos.");
        setHistoryDocuments([]);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    fetchProjetos();
  }, []);

  // Exibe uma notificacao temporaria na interface.
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
      uploadedFilesRef.current.filter((document) => document.id !== documentId),
    );
  };

  // Limpa todos os arquivos pendentes de upload.
  const clearUploadedFiles = () => {
    syncUploadedFiles([]);
  };

  // Gera o documento final e usa os dados do projeto quando vierem do upload.
  const completeProcessing = (
    apiResults: ProcessingResult[] = [],
    projectInput?: ProjectSaveInput,
    sourceFiles?: UploadDocument[],
  ) => {
    const filesToProcess = sourceFiles?.length
      ? sourceFiles
      : uploadedFilesRef.current;

    if (filesToProcess.length === 0) {
      return null;
    }

    const baseDocument: GeneratedDocument = {
      ...buildGeneratedDocumentFromUploads(filesToProcess),
      file_urls: apiResults.map((result) => result.file_url),
    };
    const projectInfo = projectInput ? buildProjectInfo(projectInput) : null;
    const generatedDocument: GeneratedDocument = projectInfo
      ? {
          ...baseDocument,
          title: `Memorial de cálculo - ${projectInfo.name}`,
          createdAt: new Date().toLocaleDateString("pt-BR"),
          projectInfo,
        }
      : baseDocument;

    setCurrentDocument(generatedDocument);
    setShouldPromptProjectSave(!projectInfo);

    if (projectInfo) {
      const historyDocument =
        buildHistoryDocumentFromGenerated(generatedDocument);

      setHistoryDocuments((currentHistory) => [
        historyDocument,
        ...currentHistory.filter(
          (document) => document.document.id !== generatedDocument.id,
        ),
      ]);
    }

    syncUploadedFiles([]);
    showToast(
      projectInfo
        ? "Processamento concluído e projeto salvo no histórico."
        : "Processamento concluído com sucesso.",
      "success",
    );

    return generatedDocument;
  };

  // Salva ou atualiza as informações do projeto no documento atual.
  const saveCurrentProject = (projectInput: ProjectSaveInput) => {
    if (!currentDocument) {
      showToast("Nenhum documento disponível para salvar.", "error");
      return;
    }

    const projectInfo = buildProjectInfo(projectInput);
    const savedDocument: GeneratedDocument = {
      ...currentDocument,
      title: `Memorial de cálculo - ${projectInfo.name}`,
      createdAt: new Date().toLocaleDateString("pt-BR"),
      projectInfo,
    };
    const historyDocument = buildHistoryDocumentFromGenerated(savedDocument);

    setCurrentDocument(savedDocument);
    setShouldPromptProjectSave(false);
    setHistoryDocuments((currentHistory) => [
      historyDocument,
      ...currentHistory.filter(
        (document) => document.document.id !== savedDocument.id,
      ),
    ]);
    showToast("Projeto salvo no histórico.", "success");
  };

  // Abre um documento do histórico na área de resultado.
  const openHistoryPreview = (documentId: string) => {
    const historyDocument = historyDocuments.find(
      (document) => document.id === documentId,
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
      currentHistory.filter((document) => document.id !== documentId),
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

  const simulatePreviewAction = (fileName: string) => {
    const selectedUpload = uploadedFilesRef.current.find(
      (document) => document.name === fileName,
    );

    if (!selectedUpload?.file) {
      showToast(`Pré-visualização de ${fileName} indisponível.`, "info");
      return;
    }

    if (selectedUpload.kind !== "pdf") {
      showToast(
        `Pré-visualização de ${selectedUpload.kind.toUpperCase()} ainda não está disponível no navegador.`,
        "info",
      );
      return;
    }

    const objectUrl = window.URL.createObjectURL(selectedUpload.file);
    const previewWindow = window.open(
      objectUrl,
      "_blank",
      "noopener,noreferrer",
    );

    window.setTimeout(() => {
      window.URL.revokeObjectURL(objectUrl);
    }, 1000);

    showToast(
      previewWindow
        ? `Pré-visualização de ${fileName} aberta.`
        : "Permita pop-ups para abrir a pré-visualização.",
      previewWindow ? "success" : "error",
    );
  };

  const addTechnicalStandards = (
    fileList: FileList | File[],
  ): AddFilesResult => {
    const incomingFiles = Array.from(fileList);
    const parsedStandards = incomingFiles.map(buildTechnicalStandard);
    const knownNames = new Set(
      technicalStandards.map((standard) => standard.name.toLowerCase()),
    );
    const nextStandards = [...technicalStandards];
    let duplicateCount = 0;
    let invalidCount = 0;
    let addedCount = 0;

    parsedStandards.forEach((standard) => {
      if (!standard) {
        invalidCount += 1;
        return;
      }

      const standardKey = standard.name.toLowerCase();

      if (knownNames.has(standardKey)) {
        duplicateCount += 1;
        return;
      }

      knownNames.add(standardKey);
      nextStandards.push(standard);
      addedCount += 1;
    });

    if (addedCount > 0) {
      setTechnicalStandards(nextStandards);
      showToast(
        addedCount === 1
          ? "Norma adicionada e habilitada para a IA."
          : `${addedCount} normas adicionadas e habilitadas para a IA.`,
        "success",
      );
    } else if (invalidCount > 0) {
      showToast("Somente normas em PDF são aceitas.", "error");
    } else if (duplicateCount > 0) {
      showToast("As normas selecionadas já estavam na lista.", "info");
    }

    return { addedCount, duplicateCount, invalidCount };
  };

  const toggleStandard = (standardId: string) => {
    const selectedStandard = technicalStandards.find(
      (standard) => standard.id === standardId,
    );

    if (!selectedStandard) {
      showToast("Norma não encontrada.", "error");
      return;
    }

    setTechnicalStandards((currentStandards) =>
      currentStandards.map((standard) =>
        standard.id === standardId
          ? { ...standard, enabled: !standard.enabled }
          : standard,
      ),
    );
    showToast(
      `${selectedStandard.code} ${
        selectedStandard.enabled ? "desabilitada" : "habilitada"
      } para consulta da IA.`,
      "info",
    );
  };

  const downloadStandard = (standardId: string) => {
    const selectedStandard = technicalStandards.find(
      (standard) => standard.id === standardId,
    );

    if (!selectedStandard) {
      showToast("Norma indisponível para download.", "error");
      return;
    }

    if (selectedStandard.file) {
      const objectUrl = window.URL.createObjectURL(selectedStandard.file);
      const link = document.createElement("a");

      link.href = objectUrl;
      link.download = selectedStandard.file.name;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(objectUrl);
    }

    showToast(`Download de ${selectedStandard.code} iniciado.`, "success");
  };

  // Baixa o arquivo gerado pelo backend.
  const downloadDocumentAsset = async (
    url: string | undefined,
    label: string,
  ) => {
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
        technicalStandards,
        isLoadingHistory,
        historyError,
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
        addTechnicalStandards,
        toggleStandard,
        downloadStandard,
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
