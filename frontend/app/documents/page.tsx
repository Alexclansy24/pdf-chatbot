import DocumentList from "@/components/documents/document-list";

export default function DocumentsPage() {
  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Documents
          </h1>

          <p className="mt-2 text-muted-foreground">
            Manage your uploaded PDF documents.
          </p>
        </div>

        <DocumentList />
      </div>
    </main>
  );
}