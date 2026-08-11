
import { api } from "@/lib/api";
import { Document } from "@/types/document";

export async function getDocuments(): Promise<Document[]> {
  const response = await api.get("/documents");

  return response.data;
}
export async function deleteDocument(
  documentId: string
): Promise<void> {
  await api.delete(`/documents/${documentId}`);
}