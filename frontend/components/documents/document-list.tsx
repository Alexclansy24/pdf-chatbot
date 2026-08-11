"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  deleteDocument,
  getDocuments,
} from "@/services/documents";

export default function DocumentList() {
  const queryClient = useQueryClient();

  const {
    data: documents,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["documents"],
    queryFn: getDocuments,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["documents"],
      });
    },
  });

  const handleDelete = (documentId: string) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmed) {
      return;
    }

    deleteMutation.mutate(documentId);
  };

  if (isLoading) {
    return (
      <div className="rounded-lg border p-6">
        Loading documents...
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-lg border border-red-200 p-6 text-red-600">
        Failed to load documents.
      </div>
    );
  }

  if (!documents || documents.length === 0) {
    return (
      <div className="rounded-lg border p-10 text-center">
        <h3 className="text-lg font-semibold">
          No documents
        </h3>

        <p className="mt-2 text-sm text-muted-foreground">
          Upload your first PDF to get started.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {documents.map((document) => (
        <div
          key={document.id}
          className="flex items-center justify-between rounded-lg border p-4"
        >
          <div>
            <h3 className="font-medium">
              {document.filename}
            </h3>

            <div className="mt-1 text-sm text-muted-foreground">
              {document.page_count ?? 0} pages
              {" · "}
              {document.chunk_count ?? 0} chunks
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="rounded-full bg-muted px-3 py-1 text-sm">
              {document.status}
            </span>

            <button
              type="button"
              onClick={() =>
                handleDelete(document.id)
              }
              disabled={deleteMutation.isPending}
              className="rounded-md border px-3 py-1 text-sm text-red-600 hover:bg-red-50 disabled:opacity-50"
            >
              {deleteMutation.isPending
                ? "Deleting..."
                : "Delete"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}