export type FileKind = "dwg" | "dxf" | "pdf" | "xml";

export type ToastTone = "success" | "error" | "info";

export type UploadStatusTone = "success" | "error" | "info";

export interface UploadDocument {
  id: string;
  name: string;
  kind: FileKind;
  file: File;
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
}

export interface HistoryDocument {
  id: string;
  name: string;
  kind: FileKind;
  date: string;
  size: string;
  document: GeneratedDocument;
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
