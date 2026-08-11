export interface ChatRequest {
  document_id: string;
  question: string;
}

export interface ChatSource {
  page: number;
  content: string;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}