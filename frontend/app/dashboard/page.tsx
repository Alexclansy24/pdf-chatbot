"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";

import DashboardHeader from "@/components/dashboard/dashboard-header";
import StatsCards from "@/components/dashboard/stats-cards";
import RecentDocuments from "@/components/dashboard/recent-documents";

import { getDocuments } from "@/services/documents";
import { Document } from "@/types/document";
import { isAuthenticated } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();

  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }

    async function loadDocuments() {
      try {
        setLoading(true);

        const data = await getDocuments();

        setDocuments(data);
      } catch (error) {
        console.error(error);

        setError(
          "Failed to load your documents."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDocuments();
  }, [router]);

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">
              Dashboard
            </h2>

            <p className="mt-1 text-muted-foreground">
              Manage your documents and chat with your PDFs.
            </p>
          </div>

          <div className="flex gap-3">
            <Button
              variant="outline"
              onClick={() => router.push("/documents")}
            >
              Documents
            </Button>

            <Button
              onClick={() => router.push("/chat")}
            >
              Open Chat
            </Button>
          </div>
        </div>

        {loading ? (
          <div className="space-y-6">
            <div className="grid gap-4 md:grid-cols-3">
              <div className="h-32 animate-pulse rounded-xl border bg-muted" />
              <div className="h-32 animate-pulse rounded-xl border bg-muted" />
              <div className="h-32 animate-pulse rounded-xl border bg-muted" />
            </div>

            <div className="h-80 animate-pulse rounded-xl border bg-muted" />
          </div>
        ) : error ? (
          <div className="rounded-lg border border-destructive p-6">
            <p className="text-destructive">
              {error}
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            <StatsCards documents={documents} />

            <RecentDocuments documents={documents} />
          </div>
        )}
      </main>
    </div>
  );
}