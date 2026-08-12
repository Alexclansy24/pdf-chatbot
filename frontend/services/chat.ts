import { getToken } from "@/lib/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type StreamCallbacks = {
  onToken: (token: string) => void;
  onDone: () => void;
  onError: (error: string) => void;
};

export async function streamQuestion(
  question: string,
  callbacks: StreamCallbacks
) {
  const token = getToken();

  if (!token) {
    callbacks.onError("Authentication required.");
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/chat-stream/tokens?question=${encodeURIComponent(
        question
      )}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "text/event-stream",
        },
      }
    );

    if (response.status === 401) {
      callbacks.onError("Your session has expired. Please login again.");
      return;
    }

    if (!response.ok) {
      callbacks.onError(
        `Streaming request failed (${response.status}).`
      );
      return;
    }

    if (!response.body) {
      callbacks.onError("Streaming response body is empty.");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, {
        stream: true,
      });

      // SSE events are separated by a blank line
      const events = buffer.split(/\r?\n\r?\n/);

      // Keep incomplete event for next chunk
      buffer = events.pop() ?? "";

      for (const event of events) {
        const lines = event.split(/\r?\n/);

        let eventType = "message";
        const dataLines: string[] = [];

        for (const line of lines) {
          if (line.startsWith("event:")) {
            eventType = line
              .slice("event:".length)
              .trim();
          }

          if (line.startsWith("data:")) {
            dataLines.push(
              line.slice("data:".length).trimStart()
            );
          }
        }

        const data = dataLines.join("\n");

        console.log("SSE EVENT:", {
          eventType,
          data,
        });

        if (eventType === "token") {
          callbacks.onToken(data);
        }

        if (eventType === "done") {
          callbacks.onDone();
          return;
        }

        if (eventType === "error") {
          callbacks.onError(
            data || "Streaming error occurred."
          );
          return;
        }
      }
    }

    // Handle any remaining buffered event
    if (buffer.trim()) {
      const lines = buffer.split(/\r?\n/);

      let eventType = "message";
      const dataLines: string[] = [];

      for (const line of lines) {
        if (line.startsWith("event:")) {
          eventType = line
            .slice("event:".length)
            .trim();
        }

        if (line.startsWith("data:")) {
          dataLines.push(
            line.slice("data:".length).trimStart()
          );
        }
      }

      const data = dataLines.join("\n");

      if (eventType === "token") {
        callbacks.onToken(data);
      }

      if (eventType === "error") {
        callbacks.onError(
          data || "Streaming error occurred."
        );
        return;
      }
    }

    callbacks.onDone();
  } catch (error) {
    console.error(
      "Streaming request failed:",
      error
    );

    callbacks.onError(
      error instanceof Error
        ? error.message
        : "Network error while streaming."
    );
  }
}