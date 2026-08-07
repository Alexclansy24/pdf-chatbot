"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Document } from "@/types/document";

interface RecentDocumentsProps {
  documents: Document[];
}

export default function RecentDocuments({
  documents,
}: RecentDocumentsProps) {
  const router = useRouter();

  const recentDocuments = documents.slice(0, 5);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Recent Documents</CardTitle>

        <Button
          variant="outline"
          onClick={() => router.push("/documents")}
        >
          View All
        </Button>
      </CardHeader>

      <CardContent>
        {recentDocuments.length === 0 ? (
          <div className="py-10 text-center">
            <p className="text-sm text-muted-foreground">
              No documents uploaded yet.
            </p>

            <Button
              className="mt-4"
              onClick={() => router.push("/documents")}
            >
              Upload a PDF
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {recentDocuments.map((document) => (
              <div
                key={document.id}
                className="flex items-center justify-between rounded-lg border p-4"
              >
                <div className="min-w-0">
                  <p className="truncate font-medium">
                    {document.filename}
                  </p>

                  <p className="text-sm text-muted-foreground">
                    {document.page_count ?? 0} pages
                    {" · "}
                    {document.chunk_count ?? 0} chunks
                  </p>
                </div>

                <span
                  className={`ml-4 rounded-full px-3 py-1 text-xs font-medium ${
                    document.status === "INDEXED"
                      ? "bg-green-100 text-green-700"
                      : document.status === "FAILED"
                        ? "bg-red-100 text-red-700"
                        : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {document.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}