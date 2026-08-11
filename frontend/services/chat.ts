import {api} from "@/lib/api";
import {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";

export async function askQuestion(
  data: ChatRequest
): Promise<ChatResponse> {
  const response = await api.post(
    "/chat",
    data
  );

  return response.data;
}