import { PipelineStep } from '../types';

interface PipelineFlowProps {
  steps: PipelineStep[];
  visible: boolean;
}

const STEP_ICONS: Record<string, JSX.Element> = {
  embedding: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
    </svg>
  ),
  retrieval: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
    </svg>
  ),
  generation: (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
        d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  ),
};

const STEP_LABELS: Record<string, string> = {
  embedding: 'Embed Query',
  retrieval: 'Vector DB',
  generation: 'LLM Generate',
};

function StepNode({ step }: { step: PipelineStep }) {
  const icon = STEP_ICONS[step.step] || STEP_ICONS.embedding;
  const label = step.label || STEP_LABELS[step.step] || step.step;

  const statusStyles = {
    pending: 'border-dark-700 bg-dark-800/50 text-dark-500',
    active: 'border-primary-500 bg-primary-600/20 text-primary-400 shadow-lg shadow-primary-500/10',
    done: 'border-green-500/50 bg-green-600/10 text-green-400',
  };

  return (
    <div className="flex flex-col items-center gap-1 min-w-0">
      <div
        className={`relative flex items-center justify-center w-10 h-10 rounded-xl border-2 transition-all duration-300 ${statusStyles[step.status]}`}
      >
        {step.status === 'active' && (
          <div className="absolute inset-0 rounded-xl border-2 border-primary-400 animate-ping opacity-30" />
        )}
        {step.status === 'done' ? (
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
          </svg>
        ) : (
          icon
        )}
      </div>
      <span className="text-[10px] font-medium whitespace-nowrap">{label}</span>
      {step.status === 'done' && step.duration_ms != null && (
        <span className="text-[9px] text-dark-500">{step.duration_ms}ms</span>
      )}
      {step.status === 'done' && step.detail?.chunks_found != null && (
        <span className="text-[9px] text-green-500">{step.detail.chunks_found} chunks</span>
      )}
      {step.status === 'done' && step.detail?.tokens != null && (
        <span className="text-[9px] text-green-500">{step.detail.tokens} tokens</span>
      )}
    </div>
  );
}

function Arrow({ active }: { active: boolean }) {
  return (
    <div className="flex items-center px-1 mt-[-18px]">
      <div className={`h-0.5 w-6 transition-colors duration-300 ${active ? 'bg-primary-500' : 'bg-dark-700'}`} />
      <div
        className={`w-0 h-0 border-t-[4px] border-t-transparent border-b-[4px] border-b-transparent border-l-[6px] transition-colors duration-300 ${
          active ? 'border-l-primary-500' : 'border-l-dark-700'
        }`}
      />
    </div>
  );
}

export default function PipelineFlow({ steps, visible }: PipelineFlowProps) {
  if (!visible || steps.length === 0) return null;

  const allDone = steps.every(s => s.status === 'done');
  const totalMs = steps.reduce((sum, s) => sum + (s.duration_ms || 0), 0);

  return (
    <div className={`border-t border-dark-700 bg-dark-900/80 backdrop-blur-sm px-4 py-3 transition-all duration-500 ${
      allDone ? 'opacity-80' : 'opacity-100'
    }`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${allDone ? 'bg-green-500' : 'bg-primary-500 animate-pulse'}`} />
          <span className="text-[11px] font-medium text-dark-400 uppercase tracking-wider">
            RAG Pipeline
          </span>
        </div>
        {allDone && totalMs > 0 && (
          <span className="text-[10px] text-dark-500">Total: {totalMs}ms</span>
        )}
      </div>

      <div className="flex items-start justify-center gap-0">
        {steps.map((step, idx) => (
          <div key={step.step} className="flex items-start">
            <StepNode step={step} />
            {idx < steps.length - 1 && (
              <Arrow active={steps[idx + 1]?.status !== 'pending'} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
