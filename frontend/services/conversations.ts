import {api} from "@/lib/api";

export interface Conversation {
  id: string;
  title: string;
}

interface CreateConversationResponse {
  success: boolean;
  data: Conversation;
}

interface ListConversationsResponse {
  success: boolean;
  data: Conversation[];
}

export async function createConversation(
  title: string = "New Conversation"
): Promise<Conversation> {
  const response =
    await api.post<CreateConversationResponse>(
      "/conversations",
      {
        title,
      }
    );

  return response.data.data;
}

export async function getConversations(): Promise<
  Conversation[]
> {
  const response =
    await api.get<ListConversationsResponse>(
      "/conversations"
    );

  return response.data.data;
}