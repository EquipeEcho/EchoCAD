import {
  FileKind,
  GeneratedDocument,
  HistoryDocument,
  UploadDocument,
} from "../types/documents";

// Monta um documento de exemplo para a pre-visualizacao.
function buildPreviewDocument(
  id: string,
  title: string,
  createdAt: string,
  reference: string,
  sourceFiles: string[]
): GeneratedDocument {
  return {
    id,
    title,
    subtitle: "Pré-visualização do memorial de cálculo",
    createdAt,
    reference,
    versionLabel: "Versão 1.0 - PDF",
    summary:
      "Documento técnico gerado a partir da leitura dos arquivos estruturais enviados para a plataforma EchoCAD.",
    sourceFiles,
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
    file_urls: sourceFiles.map((fileName) => `https://example.com/files/${fileName}`), // URLs fictícias para os arquivos de origem
  };
}

export const mockUploadDocuments: UploadDocument[] = [
  { id: "upload-1", name: "Planta_Batalhao_A1.dwg", kind: "dwg", file: new File([], "Planta_Batalhao_A1.dwg") },
  { id: "upload-2", name: "Memorial_Preliminar.pdf", kind: "pdf", file: new File([], "Memorial_Preliminar.pdf") },
  { id: "upload-3", name: "Croqui_Infraestrutura.dxf", kind: "dxf", file: new File([], "Croqui_Infraestrutura.dxf") },
  { id: "upload-4", name: "Analise_Estrutural_C.xml", kind: "xml", file: new File([], "Analise_Estrutural_C.xml") },
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
      "Memorial de Cálculo - Batalhão Central",
      "20/03/2026",
      "EchoCAD-7429",
      ["Planta_Batalhao_Central.dwg", "Memorial_Base.pdf"]
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
      "Memorial de Cálculo - Bloco Administrativo A2",
      "18/03/2026",
      "EchoCAD-7310",
      ["Planta_Administrativa_A2.dwg", "Croqui_Fundacao.dxf"]
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
      "Relatório Estrutural Final - Ala Norte",
      "15/03/2026",
      "EchoCAD-7194",
      ["Ala_Norte.pdf", "Analise_Final.xml"]
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
      "Memorial de Cálculo - Rede Hidráulica",
      "10/03/2026",
      "EchoCAD-7011",
      ["Rede_Hidraulica.dxf", "Memorial_Hidraulico.pdf"]
    ),
  },
];

// Identifica o tipo do arquivo pelo nome.
export function getFileKindFromName(fileName: string): FileKind | null {
  const extension = fileName.toLowerCase().split(".").pop();

  if (
    extension !== "dwg" &&
    extension !== "dxf" &&
    extension !== "pdf" &&
    extension !== "xml"
  ) {
    return null;
  }

  return extension;
}

// Gera um documento final a partir dos uploads enviados.
export function buildGeneratedDocumentFromUploads(
  documents: UploadDocument[]
): GeneratedDocument {
  const primaryName = documents[0]?.name.replace(/\.[^.]+$/, "") || "Projeto CAD";
  const referenceSuffix = String(Date.now()).slice(-4);

  return buildPreviewDocument(
    `generated-${Date.now()}`,
    `Memorial de Cálculo - ${primaryName}`,
    "21/03/2026",
    `EchoCAD-${referenceSuffix}`,
    documents.map((document) => document.name)
  );
}

// Converte o documento gerado em item de historico.
export function buildHistoryDocumentFromGenerated(
  document: GeneratedDocument
): HistoryDocument {
  return {
    id: `history-${document.id}`,
    name: `${document.title.replace(/\s+/g, "_")}.pdf`,
    kind: "pdf",
    date: document.createdAt,
    size: "2.1 MB",
    document,
  };
}
