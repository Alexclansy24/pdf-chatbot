export type DocumentStatus =
  | "UPLOADED"
  | "PROCESSING"
  | "INDEXED"
  | "FAILED";

export interface Document {
  id: string;
  filename: string;
  status: DocumentStatus;
  page_count: number | null;
  chunk_count: number | null;
}