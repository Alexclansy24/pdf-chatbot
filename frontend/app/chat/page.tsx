import ChatInterface from "@/components/chat/chat-interface";

export default function ChatPage() {
  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Chat with your documents
          </h1>

          <p className="mt-2 text-muted-foreground">
            Select a document and ask questions
            about its contents.
          </p>
        </div>

        <ChatInterface />
      </div>
    </main>
  );
}