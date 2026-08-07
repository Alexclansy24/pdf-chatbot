import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Document } from "@/types/document";

interface StatsCardsProps {
  documents: Document[];
}

export default function StatsCards({
  documents,
}: StatsCardsProps) {
  const total = documents.length;

  const indexed = documents.filter(
    (document) => document.status === "INDEXED"
  ).length;

  const processing = documents.filter(
    (document) => document.status === "PROCESSING"
  ).length;

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Total Documents
          </CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {total}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Indexed
          </CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {indexed}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">
            Processing
          </CardTitle>
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {processing}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}