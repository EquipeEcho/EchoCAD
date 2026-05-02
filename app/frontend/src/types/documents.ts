export type FileKind = "dwg" | "dxf" | "pdf" | "xlsx";

export type ToastTone = "success" | "error" | "info";

export type UploadStatusTone = "success" | "error" | "info";

export interface UploadDocument {
  id: string;
  name: string;
  kind: FileKind;
  file?: File;
}

export interface ProjectSaveInput {
  name: string;
  cliente?: string;
  descricao?: string;
}

export interface ProjectInfo extends ProjectSaveInput {
  savedAt: string;
}

export interface PreviewTableRow {
  label: string;
  value: string;
}

export interface GeneratedDocument {
  id: string;
  title: string;
  subtitle: string;
  createdAt: string;
  reference: string;
  versionLabel: string;
  summary: string;
  previewLines: string[];
  tableRows: PreviewTableRow[];
  sourceFiles: string[];
  file_urls: string[];
  projectInfo?: ProjectInfo;
}

export interface HistoryDocument {
  id: string;
  name: string;
  kind: FileKind;
  date: string;
  size: string;
  document: GeneratedDocument;
  projectInfo?: ProjectInfo;
}

export interface TechnicalStandard {
  id: string;
  name: string;
  code: string;
  category: string;
  date: string;
  size: string;
  kind: FileKind;
  enabled: boolean;
  file?: File;
}

export interface ToastState {
  id: number;
  tone: ToastTone;
  message: string;
}

export interface AddFilesResult {
  addedCount: number;
  duplicateCount: number;
  invalidCount: number;
}
