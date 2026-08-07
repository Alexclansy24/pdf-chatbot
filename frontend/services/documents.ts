
import { api } from "@/lib/api";
import { Document } from "@/types/document";

export async function getDocuments(): Promise<Document[]> {
  const response = await api.get("/documents");

  return response.data;
}