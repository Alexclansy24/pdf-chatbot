"use client";

import { useState } from "react";

import { useQuery } from "@tanstack/react-query";

import { getDocuments } from "@/services/documents";
import { streamQuestion } from "@/services/chat";

export default function ChatInterface() {
  const [selectedDocument, setSelectedDocument] =
    useState("");

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [isStreaming, setIsStreaming] =
    useState(false);

  const [sources, setSources] = useState<any[]>([]);
  const [error, setError] =
    useState<string | null>(null);

  const {
    data: documents,
    isLoading: documentsLoading,
  } = useQuery({
    queryKey: ["documents"],
    queryFn: getDocuments,
  });

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!selectedDocument) {
      setError("Please select a document.");
      return;
    }

    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    if (isStreaming) {
      return;
    }

    setAnswer("");
    setError(null);
    setIsStreaming(true);

    try {
  await streamQuestion(
  {
    document_id: selectedDocument,
    question: question.trim(),
  },
  {
    onToken: (token) => {
      console.log(
        "TOKEN RECEIVED:",
        token,
        typeof token
      );

      setAnswer(
        (previous) =>
          previous + token
      );
    },

    onSources: (sources) => {
      console.log(
        "SOURCES:",
        sources
      );
    },

    onDone: () => {
      console.log(
        "STREAM DONE"
      );

      setIsStreaming(false);
    },

    onError: (message) => {
      console.error(
        "STREAM ERROR:",
        message
      );

      setError(message);
      setIsStreaming(false);
    },
  }
);
} catch (error) {
  console.error(
    "Chat streaming failed:",
    error
  );

  setError(
    "Failed to get an answer."
  );

  setIsStreaming(false);
}
  };

  return (
    <div className="space-y-6">

      {/* Document Selector */}

      <div className="space-y-2">

        <label
          htmlFor="document"
          className="text-sm font-medium"
        >
          Select Document
        </label>

        <select
          id="document"
          value={selectedDocument}
          onChange={(event) =>
            setSelectedDocument(
              event.target.value
            )
          }
          disabled={
            documentsLoading ||
            isStreaming
          }
          className="w-full rounded-md border bg-background px-3 py-2"
        >

          <option value="">
            Select a document
          </option>

          {documents?.map((document) => (
            <option
              key={document.id}
              value={document.id}
            >
              {document.filename}
            </option>
          ))}

        </select>

      </div>


      {/* Question Form */}

      <form
        onSubmit={handleSubmit}
        className="space-y-3"
      >

        <label
          htmlFor="question"
          className="text-sm font-medium"
        >
          Ask a question
        </label>

        <textarea
          id="question"
          value={question}
          onChange={(event) =>
            setQuestion(
              event.target.value
            )
          }
          disabled={isStreaming}
          placeholder="Ask something about your document..."
          rows={4}
          className="w-full rounded-md border bg-background p-3"
        />

        <button
          type="submit"
          disabled={
            isStreaming ||
            !selectedDocument ||
            !question.trim()
          }
          className="rounded-md bg-primary px-4 py-2 text-primary-foreground disabled:opacity-50"
        >
          {isStreaming
            ? "Thinking..."
            : "Ask Question"}
        </button>

      </form>


      {/* Error */}

      {error && (
        <div className="rounded-md border border-red-200 p-4 text-red-600">
          {error}
        </div>
      )}


      {/* Answer */}

      {(answer || isStreaming) && (
        <div className="rounded-lg border p-6">

          <h2 className="mb-3 text-lg font-semibold">
            Answer
          </h2>

          <p className="whitespace-pre-wrap text-sm leading-7">

            {answer}

            {isStreaming && (
              <span className="ml-1 animate-pulse">
                ▌
              </span>
            )}

          </p>

        </div>
      )}
      {/* Sources */}
      {sources.length > 0 && (
        <div className="rounded-lg border p-6">
          <h2 className="mb-4 text-lg font-semibold">
            Sources
          </h2>

        <div className="space-y-3">
      {sources.map((source, index) => (
        <div
          key={source.chunk_id ?? index}
          className="rounded-md bg-muted p-4"
        >
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">
              Chunk {source.chunk_index}
            </span>

            <span className="text-xs text-muted-foreground">
              Score: {source.score?.toFixed(3)}
            </span>
          </div>
        </div>
      ))}
    </div>
  </div>
)}

    </div>
  );
}