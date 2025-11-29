import { FileText } from "lucide-react"

export default function SourcesList({ sources }) {
  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
        <FileText className="w-5 h-5 text-blue-600" />
        Sources
      </h2>
      <div className="space-y-2">
        {sources.map((source, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200 hover:border-blue-300 transition-colors"
          >
            <div className="flex items-center gap-3 flex-1">
              <FileText className="w-4 h-4 text-slate-600" />
              <span className="text-sm font-medium text-slate-900">{source.document}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-semibold">
                Dist: {source.score.toFixed(4)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
