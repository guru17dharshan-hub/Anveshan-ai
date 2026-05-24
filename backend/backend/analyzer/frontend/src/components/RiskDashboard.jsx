export default function RiskDashboard({ result }) {
  const { risk_score, risk_level, explanation, layers } = result;

  const levelColor = {
    HIGH:   "text-red-400 bg-red-950 border-red-500",
    MEDIUM: "text-yellow-400 bg-yellow-950 border-yellow-500",
    LOW:    "text-green-400 bg-green-950 border-green-500",
  }[risk_level];

  const levelIcon = { HIGH: "🔴", MEDIUM: "🟡", LOW: "🟢" }[risk_level];

  return (
    <div className="mt-8 space-y-6">

      {/* Risk Score Banner */}
      <div className={`border rounded-xl p-6 text-center ${levelColor}`}>
        <div className="text-5xl mb-2">{levelIcon}</div>
        <div className="text-3xl font-bold">{risk_score}/100</div>
        <div className="text-xl font-semibold mt-1">{risk_level} RISK</div>
      </div>

      {/* AI Explanation */}
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
        <h3 className="text-blue-400 font-semibold mb-3 text-sm uppercase tracking-widest">
          AI Analysis
        </h3>
        <p className="text-gray-300 leading-relaxed">{explanation}</p>
      </div>

      {/* Layer Breakdown */}
      <div className="grid grid-cols-2 gap-4">
        {[
          { key: "visual",   label: "Visual Forensics",   icon: "🔬" },
          { key: "ocr",      label: "OCR Intelligence",   icon: "📝" },
          { key: "metadata", label: "Metadata Forensics", icon: "📋" },
          { key: "anomaly",  label: "Anomaly Score",      icon: "🌲" },
        ].map(({ key, label, icon }) => (
          <div key={key} className="bg-gray-900 border border-gray-700 rounded-xl p-4">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">
              {icon} {label}
            </div>
            <div className="text-2xl font-bold text-white mb-2">
              {layers[key]?.score ?? 0}
              <span className="text-sm text-gray-500">/100</span>
            </div>
            <ul className="space-y-1">
              {(layers[key]?.flags || []).map((flag, i) => (
                <li key={i} className="text-xs text-gray-400">▸ {flag}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Escalate Button */}
      {risk_level === "HIGH" && (
        <button className="w-full bg-red-700 hover:bg-red-600 text-white
                           py-3 rounded-xl font-semibold transition-all">
          Escalate to Compliance Team
        </button>
      )}

    </div>
  );
}
