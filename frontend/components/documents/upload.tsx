"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {api} from "@/lib/api";

function getUploadError(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return "Failed to upload PDF.";
  }

  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (
          item &&
          typeof item === "object" &&
          "msg" in item
        ) {
          return String(item.msg);
        }

        return "Validation error";
      })
      .join(", ");
  }

  return "Failed to upload PDF.";
}

interface UploadProps {
  onUploaded?: () => void;
}

export default function Upload({
  onUploaded,
}: UploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  function handleFileSelect(
    selectedFile: File | undefined
  ) {
    setError("");
    setSuccess("");

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }

    setFile(selectedFile);
  }

  function handleInputChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    handleFileSelect(event.target.files?.[0]);
  }

  async function handleUpload() {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    setUploading(true);
    setProgress(0);
    setError("");
    setSuccess("");

    try {
      const formData = new FormData();

      formData.append("file", file);

      await api.post(
        "/ingestion/pdf",
        formData,
        {
          onUploadProgress: (event) => {
            if (!event.total) {
              return;
            }

            const percentage = Math.round(
              (event.loaded * 100) / event.total
            );

            setProgress(percentage);
          },
        }
      );

      setProgress(100);
      setSuccess("PDF uploaded successfully.");
      setFile(null);
      onUploaded?.();

      if (inputRef.current) {
        inputRef.current.value = "";
      }

    } catch (error) {
      console.error(error);

      setError(getUploadError(error));
    } finally {
      setUploading(false);
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload PDF</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          onChange={handleInputChange}
          disabled={uploading}
          className="block w-full text-sm"
        />

        {file && (
          <div className="rounded-lg border p-4">
            <p className="font-medium">
              {file.name}
            </p>

            <p className="text-sm text-muted-foreground">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
        )}

        {uploading && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Uploading...</span>
              <span>{progress}%</span>
            </div>

            <div className="h-2 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full bg-primary transition-all"
                style={{
                  width: `${progress}%`,
                }}
              />
            </div>
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-destructive p-3 text-sm text-destructive">
            {error}
          </div>
        )}

        {success && (
          <div className="rounded-lg border p-3 text-sm">
            {success}
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="w-full"
        >
          {uploading
            ? "Uploading..."
            : "Upload PDF"}
        </Button>
      </CardContent>
    </Card>
  );
}