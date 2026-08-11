export interface ChatRequest {
  document_id: string;
  conversation_id: string;
  question: string;
}
export interface ChatSource {
  document_id: string;
  chunk_id: string;
  chunk_index: number;
  score: number;
}

export interface ChatData {
  question: string;
  context: string;
  answer: string;
  retrieved_chunks: number;
  sources: ChatSource[];
  chat_history: string;
}

export interface ChatResponse {
  success: boolean;
  data: ChatData;
}