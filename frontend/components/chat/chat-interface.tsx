"use client";

import { useState } from "react";

import {
  useMutation,
  useQuery,
} from "@tanstack/react-query";

import {
  getDocuments,
} from "@/services/documents";

import {
  askQuestion,
} from "@/services/chat";

import {
  ChatResponse,
} from "@/types/chat";

export default function ChatInterface() {
  const [selectedDocument, setSelectedDocument] =
    useState("");

  const [question, setQuestion] =
    useState("");

  const [response, setResponse] =
    useState<ChatResponse | null>(null);

  const {
    data: documents,
    isLoading: documentsLoading,
  } = useQuery({
    queryKey: ["documents"],
    queryFn: getDocuments,
  });

  const chatMutation = useMutation({
    mutationFn: askQuestion,

    onSuccess: (data) => {
      setResponse(data);
    },
  });

  const handleSubmit = (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!selectedDocument) {
      return;
    }

    if (!question.trim()) {
      return;
    }

    setResponse(null);

    chatMutation.mutate({
      document_id: selectedDocument,
      question: question.trim(),
    });
  };

  return (
    <div className="space-y-6">
      {/* Document selector */}

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
          disabled={documentsLoading}
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

      {/* Question form */}

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
            setQuestion(event.target.value)
          }
          placeholder="Ask something about your document..."
          rows={4}
          className="w-full rounded-md border bg-background p-3"
        />

        <button
          type="submit"
          disabled={
            chatMutation.isPending ||
            !selectedDocument ||
            !question.trim()
          }
          className="rounded-md bg-primary px-4 py-2 text-primary-foreground disabled:opacity-50"
        >
          {chatMutation.isPending
            ? "Thinking..."
            : "Ask Question"}
        </button>
      </form>

      {/* Error */}

      {chatMutation.isError && (
        <div className="rounded-md border border-red-200 p-4 text-red-600">
          Failed to get an answer.
        </div>
      )}

      {/* Answer */}

      {response && (
        <div className="space-y-6">
          <div className="rounded-lg border p-6">
            <h2 className="mb-3 text-lg font-semibold">
              Answer
            </h2>

            <p className="whitespace-pre-wrap text-sm leading-7">
              {response.answer}
            </p>
          </div>

          {/* Sources */}

          {response.sources?.length > 0 && (
            <div className="rounded-lg border p-6">
              <h2 className="mb-4 text-lg font-semibold">
                Sources
              </h2>

              <div className="space-y-4">
                {response.sources.map(
                  (source, index) => (
                    <div
                      key={index}
                      className="rounded-md bg-muted p-4"
                    >
                      <div className="mb-2 text-sm font-medium">
                        Page {source.page}
                      </div>

                      <p className="text-sm text-muted-foreground">
                        {source.content}
                      </p>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}