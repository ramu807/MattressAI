import { useState } from 'react';
import { Source } from '../types';

interface SourceCardProps {
  source: Source;
  index: number;
}

export default function SourceCard({ source, index }: SourceCardProps) {
  const [expanded, setExpanded] = useState(false);
  const scorePercent = Math.round(source.relevance_score * 100);

  const scoreColor =
    scorePercent >= 80 ? 'text-green-400 bg-green-400/10' :
    scorePercent >= 60 ? 'text-yellow-400 bg-yellow-400/10' :
    'text-orange-400 bg-orange-400/10';

  return (
    <div className="border border-dark-700 rounded-lg overflow-hidden bg-dark-800/50">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-3 py-2 flex items-center justify-between text-left hover:bg-dark-700/50 transition-colors"
      >
        <div className="flex items-center gap-2 min-w-0">
          <span className="flex-shrink-0 w-5 h-5 rounded bg-primary-600/20 text-primary-400 text-xs flex items-center justify-center font-medium">
            {index + 1}
          </span>
          <span className="text-sm text-dark-200 truncate">{source.source}</span>
          <span className="flex-shrink-0 text-xs text-dark-400">p.{source.page}</span>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0 ml-2">
          <span className={`text-xs px-1.5 py-0.5 rounded ${scoreColor}`}>
            {scorePercent}%
          </span>
          <svg
            className={`w-4 h-4 text-dark-400 transition-transform ${expanded ? 'rotate-180' : ''}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {expanded && (
        <div className="px-3 pb-3 border-t border-dark-700">
          <p className="text-xs text-dark-300 mt-2 leading-relaxed whitespace-pre-wrap">
            {source.text}
          </p>
        </div>
      )}
    </div>
  );
}
