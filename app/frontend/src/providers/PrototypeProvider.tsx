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
import { processProject, getProjectResult, getProjeto, listProjetos, API_BASE_URL } from "../services/api";

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
  isAIProcessing: boolean;
  processingLogs: string[];
  activeProjectData: { projectId: number; projectInfo: ProjectSaveInput; files: UploadDocument[] } | null;
  addUploadedFiles: (fileList: FileList | File[]) => AddFilesResult;
  removeUploadedFile: (documentId: string) => void;
  clearUploadedFiles: () => void;
  startAIProcessing: (projectId: number, projectInfo: ProjectSaveInput, files: UploadDocument[]) => Promise<void>;
  completeProcessing: (
    apiResults?: any[],
    projectInfo?: ProjectSaveInput,
    sourceFiles?: UploadDocument[],
  ) => GeneratedDocument | null;
  saveCurrentProject: (projectInfo: ProjectSaveInput) => void;
  openHistoryPreview: (documentId: string) => void;
  removeHistoryDocument: (documentId: string) => void;
  downloadHistoryBundle: () => void;
  addTechnicalStandards: (fileList: FileList | File[]) => AddFilesResult;
  toggleStandard: (standardId: string) => Promise<void>;
  downloadStandard: (standardId: string) => void;
  simulatePreviewAction: (fileName: string) => void;
  downloadDocumentAsset: (url: string | undefined, label: string) => Promise<void>;
  refreshCurrentDocument: (projectId: number) => Promise<void>;
  showToast: (message: string, tone?: ToastTone) => void;
};

const PrototypeContext = createContext<PrototypeContextValue | null>(null);

type ProjetoApiItem = {
  id?: number | string;
  name?: string;
  description?: string | null;
  client?: string | null;
  created_at?: string | null;
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
    [],
  );
  const [currentDocument, setCurrentDocument] = useState<GeneratedDocument | null>(
    null
  );
  const [shouldPromptProjectSave, setShouldPromptProjectSave] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);
  const [isAIProcessing, setIsAIProcessing] = useState(false);
  const [processingLogs, setProcessingLogs] = useState<string[]>([]);
  const [activeProjectData, setActiveProjectData] = useState<{ projectId: number; projectInfo: ProjectSaveInput; files: UploadDocument[] } | null>(null);

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
        const projetos = await listProjetos();

        const normalizedHistory = projetos.map((projeto) => {
          const projectId = String(projeto.id ?? `projeto-${Math.random()}`);
          const createdAt = projeto.created_at
            ? new Date(projeto.created_at)
            : new Date();
          const previewLines = [
            projeto.description?.trim() || "Sem descrição informada.",
            `Cliente: ${projeto.client?.trim() || "Não informado"}`,
          ];

          return {
            id: projectId,
            name: projeto.name?.trim() || `Projeto ${projectId}`,
            kind: "pdf" as const,
            date: createdAt.toLocaleDateString("pt-BR"),
            size: "N/A",
            document: {
              id: projectId,
              title: projeto.name?.trim() || `Projeto ${projectId}`,
              subtitle: "Projeto cadastrado no banco de dados",
              createdAt: createdAt.toLocaleString("pt-BR"),
              reference: `PROJ-${projectId}`,
              versionLabel: "v1",
              summary: projeto.description?.trim() || "Projeto sem descrição.",
              previewLines,
              tableRows: [],
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

  const startAIProcessing = async (projectId: number, projectInfo: ProjectSaveInput, files: UploadDocument[]) => {
    if (isAIProcessing) return;
    
    setIsAIProcessing(true);
    setProcessingLogs(["Iniciando pipeline de processamento..."]);
    setActiveProjectData({ projectId, projectInfo, files });
    
    try {
      const response = await processProject(projectId, true) as Response;
      
      if (!response.body) {
        throw new Error("Resposta sem corpo");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value);
        
        const lines = chunkValue.split("\n\n");
        lines.forEach(line => {
          if (line.trim().startsWith("data: ")) {
            const message = line.trim().replace("data: ", "").replace(/\\n/g, "\n");
            if (message === "[DONE]") return;
            setProcessingLogs(prev => [...prev, message]);
          }
        });
      }

      const finalResult = await getProjectResult(projectId);
      completeProcessing(finalResult || [], projectInfo, files);
    } catch (error) {
      console.error("Erro no processamento real:", error);
      setProcessingLogs(prev => [...prev, "ERRO: Falha na comunicação com o servidor."]);
      showToast("Erro no processamento da IA", "error");
    } finally {
      setIsAIProcessing(false);
      // Mantemos o activeProjectData até que o usuário veja o resultado ou inicie outro
    }
  };

  // Limpa todos os arquivos pendentes de upload.
  const clearUploadedFiles = () => {
    syncUploadedFiles([]);
  };

  // Gera o documento final e usa os dados do projeto quando vierem do upload.
  const completeProcessing = (
    apiResults: any[] = [],
    projectInput?: ProjectSaveInput,
    sourceFiles?: UploadDocument[],
  ) => {
    let baseDocument: GeneratedDocument;

    const filesToProcess = sourceFiles?.length
      ? sourceFiles
      : uploadedFilesRef.current;

    if (filesToProcess.length > 0) {
      baseDocument = {
        ...buildGeneratedDocumentFromUploads(filesToProcess),
        file_urls: apiResults.map((result) => result.file_url).filter(Boolean),
      };
    } else if (currentDocument) {
      baseDocument = {
        ...currentDocument,
        file_urls: apiResults.map((result) => result.file_url).filter(Boolean),
      };
    } else {
      return null;
    }

    // Mapear resultados reais da IA para o documento
    if (apiResults.length > 0) {
      const tableRows: { label: string; value: string }[] = [];
      const previewLines: string[] = [];

      apiResults.forEach((res) => {
        try {
          // A IA retorna o JSON dentro de uma string (response.content)
          // Precisamos tentar extrair o JSON puro se houver lixo em volta
          const rawResult = res.resultado || "";
          const jsonMatch = rawResult.match(/\{[\s\S]*\}/);
          const aiJson = jsonMatch ? JSON.parse(jsonMatch[0]) : null;

          if (aiJson) {
            // Se tiver resumo_executivo, usamos ele
            const resumo = aiJson.resumo_executivo || aiJson;
            Object.entries(resumo).forEach(([key, value]) => {
              tableRows.push({
                label: key,
                value: typeof value === "object" ? JSON.stringify(value) : String(value),
              });
            });
            
            if (aiJson.sintese) {
               previewLines.push(aiJson.sintese);
            }
          }
        } catch (e) {
          console.warn("Falha ao parsear JSON da IA:", e);
        }
      });

      if (tableRows.length > 0) {
        baseDocument.tableRows = tableRows;
        baseDocument.summary = "Memorial gerado automaticamente via análise de IA sobre as plantas fornecidas.";
      } else {
        baseDocument.summary = "Arquivo não processado corretamente ou formato de saída da IA incompatível.";
      }
      
      if (previewLines.length > 0) {
        baseDocument.previewLines = previewLines;
      }
    } else {
      baseDocument.summary = "Arquivo não processado (nenhum resultado da IA disponível).";
    }

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

    /*if (projectInfo) {
      const historyDocument =
      buildHistoryDocumentFromGenerated(generatedDocument);

      setHistoryDocuments((currentHistory) => [
        historyDocument,
        ...currentHistory.filter(
          (document) => document.document.id !== generatedDocument.id,
        ),
      ]);
    }*/

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
  const openHistoryPreview = async (documentId: string) => {
    const historyDocument = historyDocuments.find(
      (document) => document.id === documentId,
    );

    if (!historyDocument) {
      showToast("Documento não encontrado.", "error");
      return;
    }

    // Tentar buscar resultado real da IA se for um ID numérico
    const numericId = parseInt(documentId);
    if (!isNaN(numericId)) {
      try {
        const apiResults = await getProjectResult(numericId);
        if (apiResults) {
          // Re-processar para preencher tableRows
          const projectInfo: ProjectSaveInput = {
            name: historyDocument.document.projectInfo?.name || historyDocument.name,
            cliente: historyDocument.document.projectInfo?.cliente,
            descricao: historyDocument.document.projectInfo?.descricao,
          };
          
          // Re-aproveitar completeProcessing mas sem navegar
          const sourceFiles = uploadedFilesRef.current.length > 0 
            ? uploadedFilesRef.current 
            : historyDocument.document.sourceFiles.map(name => ({ name, kind: "dxf" } as any));

          completeProcessing(apiResults, projectInfo, sourceFiles);
          return;
        }
      } catch (e) {
        console.warn("Sem resultado de IA para este item do histórico");
      }
    }

    setCurrentDocument(historyDocument.document);
    setShouldPromptProjectSave(false);
  };

  // Remove um item do histórico salvo E do banco de dados.
  const removeHistoryDocument = async (documentId: string) => {
    try {
      // Chamada DELETE para o backend remover projeto e arquivos
      const response = await fetch(
        `${API_BASE_URL}/project/?projeto_id=${documentId}`,
        { method: "DELETE" }
      );

      if (!response.ok) {
        const errorData = await response.json();
        showToast(
          `Erro ao remover projeto: ${errorData.detail || "Erro desconhecido"}`,
          "error"
        );
        return;
      }

      // Remove do estado local após sucesso
      setHistoryDocuments((currentHistory) =>
        currentHistory.filter((document) => document.id !== documentId),
      );
      showToast("Projeto removido com sucesso (pasta renomeada para .deleted).", "success");
    } catch (error) {
      console.error("Erro ao remover projeto:", error);
      showToast(
        "Erro ao remover projeto. Verifique se o backend está online.",
        "error"
      );
    }
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

  const toggleStandard = async (standardId: string) => {
    const selectedStandard = technicalStandards.find(
      (standard) => standard.id === standardId,
    );

    if (!selectedStandard) {
      showToast("Norma não encontrada.", "error");
      return;
    }

    // Extrair ID numérico se for um ID de banco (string de números)
    const normaId = /^\d+$/.test(standardId) ? standardId : null;

    // Se é uma norma do banco, chamar backend
    if (normaId) {
      try {
        const response = await fetch(
          `${API_BASE_URL}/norma/${normaId}/toggle`,
          { method: "PATCH" }
        );

        if (!response.ok) {
          const errorData = await response.json();
          showToast(
            `Erro ao atualizar norma: ${errorData.detail || "Erro desconhecido"}`,
            "error"
          );
          return;
        }

        const updatedNorma = await response.json();
        
        // Atualizar estado local com o resultado do backend
        setTechnicalStandards((currentStandards) =>
          currentStandards.map((standard) =>
            standard.id === standardId
              ? { ...standard, enabled: updatedNorma.ativo }
              : standard,
          ),
        );
        
        showToast(
          `${selectedStandard.code} ${
            updatedNorma.ativo ? "ativada" : "desativada"
          } para consulta da IA.`,
          "success",
        );
      } catch (error) {
        console.error("Erro ao atualizar norma:", error);
        showToast(
          "Erro ao atualizar norma. Verifique se o backend está online.",
          "error"
        );
      }
    } else {
      // Para normas locais (em memória), apenas atualizar estado
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
    }
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

  const refreshCurrentDocument = async (projectId: number) => {
    try {
      // 1. Buscar dados básicos do projeto
      const projeto = await getProjeto(projectId);
      
      // 2. Tentar buscar resultados da IA
      const apiResults = await getProjectResult(projectId);
      
      const projectInput: ProjectSaveInput = {
        name: projeto.name,
        cliente: projeto.client || undefined,
        descricao: projeto.description || undefined,
      };

      // Simular sourceFiles para o buildGeneratedDocument
      const sourceFiles = projeto.description?.includes("Arquivos:") 
        ? projeto.description.split("Arquivos:")[1].split(",").map(s => s.trim())
        : [];

      // Usamos completeProcessing para atualizar o currentDocument
      completeProcessing(apiResults || [], projectInput, sourceFiles.map(name => ({ name, kind: "dxf" } as any)));
      
    } catch (error) {
      console.error("Erro ao atualizar documento:", error);
      showToast("Não foi possível carregar os dados do projeto.", "error");
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
        isAIProcessing,
        processingLogs,
        activeProjectData,
        addUploadedFiles,
        removeUploadedFile,
        clearUploadedFiles,
        startAIProcessing,
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
        refreshCurrentDocument,
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
