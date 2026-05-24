import { useState } from "react";

export default function UploadBox({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [drag, setDrag] = useState(false);

  const handleFile = (f) => {
    if (f) setFile(f);
  };

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-10 text-center transition-all
        ${drag ? "border-blue-400 bg-blue-950" : "border-gray-700 bg-gray-900"}`}
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}
    >
      <div className="text-5xl mb-4">📄</div>
      <p className="text-gray-300 mb-2 font-medium">
        Drop your document here
      </p>
      <p className="text-gray-500 text-sm mb-6">
        Supports PDF, PNG, JPG — Land Records, Bank Statements, Legal Docs
      </p>

      <input
        type="file"
        accept=".pdf,.png,.jpg,.jpeg"
        className="hidden"
        id="fileInput"
        onChange={(e) => handleFile(e.target.files[0])}
      />
      <label
        htmlFor="fileInput"
        className="cursor-pointer bg-gray-800 hover:bg-gray-700 text-white
                   px-6 py-2 rounded-lg text-sm border border-gray-600 mr-3"
      >
        Browse File
      </label>

      {file && (
        <div className="mt-4 text-green-400 text-sm">
          Selected: {file.name}
        </div>
      )}

      {file && !loading && (
        <button
          onClick={() => onAnalyze(file)}
          className="mt-5 bg-blue-600 hover:bg-blue-500 text-white
                     px-8 py-3 rounded-lg font-semibold block mx-auto
                     transition-all"
        >
          Analyze Document
        </button>
      )}

      {loading && (
        <div className="mt-5 text-blue-400 animate-pulse font-medium">
          Analyzing document across 4 detection layers...
        </div>
      )}
    </div>
  );
}
