import { getToken } from "@/lib/auth";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000/api/v1";

interface StreamRequest {
  conversation_id: string;
  document_id: string;
  question: string;
}

interface StreamCallbacks {
  onToken: (token: string) => void;
  onSources?: (sources: any[]) => void;
  onDone: () => void;
  onError: (message: string) => void;
}

export async function streamQuestion(
  request: StreamRequest,
  callbacks: StreamCallbacks
) {
  const token = getToken();

  const response = await fetch(
    `${API_URL}/chat-stream/tokens`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",

        ...(token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}),
      },

      body: JSON.stringify({
        conversation_id: request.conversation_id,
        document_id: request.document_id,
        question: request.question,
      }),
    }
  );

  if (!response.ok) {
    if (response.status === 401) {
      throw new Error("Authentication required.");
    }

    throw new Error(
      `Streaming request failed: ${response.status}`
    );
  }

  if (!response.body) {
    throw new Error(
      "Streaming response body is empty."
    );
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  let buffer = "";

  try {
    while (true) {
      const { value, done } =
        await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, {
        stream: true,
      });

      const events = buffer.split("\n\n");

      buffer =
        events.pop() || "";

      for (const eventBlock of events) {
        if (!eventBlock.trim()) {
          continue;
        }

        let eventType = "message";
        let data = "";

        const lines =
          eventBlock.split("\n");

        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventType =
              line
                .slice("event:".length)
                .trim();
          }

          if (line.startsWith("data:")) {
            data +=
              line
                .slice("data:".length)
                .trim();
          }
        }

        console.log(
          "SSE:",
          eventType,
          data
        );

        // -------------------------
        // TOKEN
        // -------------------------

        if (eventType === "token") {
          let tokenText = data;

          try {
            const parsed =
              JSON.parse(data);

            if (
              typeof parsed === "string"
            ) {
              tokenText = parsed;
            } else if (
              parsed &&
              typeof parsed.token === "string"
            ) {
              tokenText = parsed.token;
            } else if (
              parsed &&
              typeof parsed.data === "string"
            ) {
              tokenText = parsed.data;
            }
          } catch {
            // data is already plain text
          }

          if (tokenText) {
            callbacks.onToken(
              tokenText
            );
          }
        }

        // -------------------------
        // SOURCES
        // -------------------------

        else if (
          eventType === "sources"
        ) {
          try {
            const sources =
              JSON.parse(data);

            callbacks.onSources?.(
              sources
            );
          } catch (error) {
            console.error(
              "Invalid sources:",
              data
            );
          }
        }

        // -------------------------
        // DONE
        // -------------------------

        else if (
          eventType === "done"
        ) {
          callbacks.onDone();
        }

        // -------------------------
        // ERROR
        // -------------------------

        else if (
          eventType === "error"
        ) {
          callbacks.onError(data);
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}