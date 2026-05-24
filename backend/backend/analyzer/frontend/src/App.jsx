import { useState } from "react";
import UploadBox from "./components/UploadBox";
import RiskDashboard from "./components/RiskDashboard";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-blue-400 mb-2">
            Anveshan AI
          </h1>
          <p className="text-gray-400 text-sm">
            अन्वेषण — Real-Time Document Forgery Detection
          </p>
          <p className="text-gray-600 text-xs mt-1">
            SuRaksha Cyber Hackathon 2.0 · Canara Bank
          </p>
        </div>

        {/* Upload */}
        <UploadBox onAnalyze={handleAnalyze} loading={loading} />

        {/* Error */}
        {error && (
          <div className="mt-6 bg-red-900 border border-red-500 rounded-lg p-4 text-red-200">
            Error: {error}
          </div>
        )}

        {/* Results */}
        {result && <RiskDashboard result={result} />}

      </div>
    </div>
  );
}
