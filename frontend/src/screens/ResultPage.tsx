import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiClient } from "../services/apiClient";
import type { DocumentDetail } from "../services/apiClient";

export default function ResultPage() {
  const { doc_id } = useParams();
  const [data, setData] = useState<DocumentDetail | null>(null);

  useEffect(() => {
    if (doc_id) {
      apiClient.getDocument(doc_id).then(setData);
    }
  }, [doc_id]);

  if (!data) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Document Result</h1>

      <pre className="bg-gray-900 text-white p-4 rounded text-sm overflow-auto">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}
