import {
  FileKind,
  GeneratedDocument,
  HistoryDocument,
  TechnicalStandard,
  UploadDocument,
} from "../types/documents";
import { formatInputDate, getTodayInputValue } from "../utils/date";

// Monta um documento de exemplo para a pré-visualização.
function buildPreviewDocument(
  id: string,
  title: string,
  createdAt: string,
  reference: string,
  sourceFiles: string[],
): GeneratedDocument {
  return {
    id,
    title,
    subtitle: "Pré-visualização do memorial de cálculo",
    createdAt,
    reference,
    versionLabel: "Versão 1.0 - XLSX",
    summary:
      "Documento técnico gerado a partir da leitura dos arquivos estruturais enviados para a plataforma EchoCAD.",
    sourceFiles,
    file_urls: sourceFiles.map(
      (fileName) => `https://example.com/files/${fileName}`,
    ),
    previewLines: [
      "Objeto: análise estrutural preliminar do conjunto administrativo.",
      "Base normativa considerada: NBR 6118, NBR 8681 e diretrizes internas do cliente.",
      "Método: consolidação de geometrias CAD, verificação de cargas e síntese documental.",
      "Escopo: memorial descritivo, memorial de cálculo e referências de elementos principais.",
    ],
    tableRows: [
      { label: "Área estimada", value: "1.240 m²" },
      { label: "Carga permanente média", value: "12,8 kN/m²" },
      { label: "Carga acidental média", value: "4,5 kN/m²" },
      { label: "Fator de combinação", value: "1,40" },
    ],
  };
}

export const mockUploadDocuments: UploadDocument[] = [
  { id: "upload-1", name: "Planta_Batalhao_A1.dwg", kind: "dwg" },
  { id: "upload-2", name: "Memorial_Preliminar.pdf", kind: "pdf" },
  { id: "upload-3", name: "Croqui_Infraestrutura.dxf", kind: "dxf" },
];
export const mockHistoryDocuments: HistoryDocument[] = [
  {
    id: "history-1",
    name: "Memorial_Batalhao_Central.pdf",
    kind: "pdf",
    date: "20/03/2026",
    size: "2.4 MB",
    document: buildPreviewDocument(
      "generated-1",
      "Memorial de cálculo - Batalhão Central",
      "20/03/2026",
      "EchoCAD-7429",
      ["Planta_Batalhao_Central.dwg", "Memorial_Base.pdf"],
    ),
  },
  {
    id: "history-2",
    name: "Planta_Administrativa_A2.dwg",
    kind: "dwg",
    date: "18/03/2026",
    size: "1.8 MB",
    document: buildPreviewDocument(
      "generated-2",
      "Memorial de cálculo - Bloco Administrativo A2",
      "18/03/2026",
      "EchoCAD-7310",
      ["Planta_Administrativa_A2.dwg", "Croqui_Fundacao.dxf"],
    ),
  },
  {
    id: "history-3",
    name: "Relatorio_Estrutural_Final.pdf",
    kind: "pdf",
    date: "15/03/2026",
    size: "45 KB",
    document: buildPreviewDocument(
      "generated-3",
      "Relatório estrutural final - Ala Norte",
      "15/03/2026",
      "EchoCAD-7194",
      ["Ala_Norte.pdf", "Analise_Final.pdf"],
    ),
  },
  {
    id: "history-4",
    name: "Croqui_Rede_Hidraulica.dxf",
    kind: "dxf",
    date: "10/03/2026",
    size: "3.1 MB",
    document: buildPreviewDocument(
      "generated-4",
      "Memorial de cálculo - Rede hidráulica",
      "10/03/2026",
      "EchoCAD-7011",
      ["Rede_Hidraulica.dxf", "Memorial_Hidraulico.pdf"],
    ),
  },
];

export const mockTechnicalStandards: TechnicalStandard[] = [
  {
    id: "standard-nbr-6118",
    name: "NBR 6118 - Projeto de estruturas de concreto",
    code: "NBR 6118",
    category: "Estrutural",
    date: "2023",
    size: "4.8 MB",
    kind: "pdf",
    enabled: true,
  },
  {
    id: "standard-nbr-5410",
    name: "NBR 5410 - Instalacoes eletricas de baixa tensao",
    code: "NBR 5410",
    category: "Eletrica",
    date: "2004",
    size: "3.6 MB",
    kind: "pdf",
    enabled: true,
  },
  {
    id: "standard-nbr-6120",
    name: "NBR 6120 - Cargas para o calculo de estruturas",
    code: "NBR 6120",
    category: "Cargas",
    date: "2019",
    size: "2.1 MB",
    kind: "pdf",
    enabled: false,
  },
  {
    id: "standard-nbr-8800",
    name: "NBR 8800 - Projeto de estruturas de aco",
    code: "NBR 8800",
    category: "Estrutural",
    date: "2008",
    size: "5.2 MB",
    kind: "pdf",
    enabled: false,
  },
];

// Identifica o tipo do arquivo pelo nome.
export function getFileKindFromName(fileName: string): FileKind | null {
  const extension = fileName.toLowerCase().split(".").pop();

  if (extension !== "dwg" && extension !== "dxf" && extension !== "pdf") {
    return null;
  }

  return extension;
}

// Gera um documento final a partir dos uploads enviados.
export function buildGeneratedDocumentFromUploads(
  documents: UploadDocument[],
): GeneratedDocument {
  const primaryName =
    documents[0]?.name.replace(/\.[^.]+$/, "") || "Projeto CAD";
  const referenceSuffix = String(Date.now()).slice(-4);
  const generatedAt = formatInputDate(getTodayInputValue());

  return buildPreviewDocument(
    `generated-${Date.now()}`,
    `Memorial de cálculo - ${primaryName}`,
    generatedAt,
    `EchoCAD-${referenceSuffix}`,
    documents.map((document) => document.name),
  );
}

// Converte o documento gerado em item de histórico.
export function buildHistoryDocumentFromGenerated(
  document: GeneratedDocument,
): HistoryDocument {
  const projectName = document.projectInfo?.name || document.title;
  const projectDate = document.projectInfo?.projectDate
    ? formatInputDate(document.projectInfo.projectDate)
    : document.createdAt;

  return {
    id: `history-${document.id}`,
    name: projectName,
    kind: "xlsx",
    date: projectDate,
    size: "2.1 MB",
    document,
    projectInfo: document.projectInfo,
  };
}
