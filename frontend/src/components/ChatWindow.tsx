import { useState, useRef, useEffect } from 'react';
import { Message, PipelineStep } from '../types';
import MessageBubble from './MessageBubble';
import PipelineFlow from './PipelineFlow';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  onSendMessage: (message: string) => void;
  onClear: () => void;
  pipelineSteps: PipelineStep[];
  pipelineVisible: boolean;
}

const SUGGESTED_QUESTIONS = [
  "What type of mattress is best for back pain?",
  "How often should I replace my mattress?",
  "What's the difference between memory foam and latex?",
  "How do I clean my mattress properly?",
];

export default function ChatWindow({ messages, isLoading, onSendMessage, onClear, pipelineSteps, pipelineVisible }: ChatWindowProps) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
      if (inputRef.current) inputRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleTextareaInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 bg-primary-600/20 rounded-2xl flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-dark-100 mb-2">Welcome to MattressAI</h2>
            <p className="text-dark-400 mb-6 max-w-md">
              Ask me anything about mattresses — types, buying advice, care tips, health considerations, and more.
              My answers are based on curated mattress knowledge documents.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg w-full">
              {SUGGESTED_QUESTIONS.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => onSendMessage(q)}
                  className="text-left text-sm px-3 py-2.5 rounded-xl border border-dark-700 bg-dark-800/50 text-dark-300 hover:bg-dark-700 hover:text-dark-100 hover:border-primary-600/50 transition-all"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map(msg => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Pipeline Flow Visualization */}
      <PipelineFlow steps={pipelineSteps} visible={pipelineVisible} />

      {/* Input Area */}
      <div className="border-t border-dark-700 bg-dark-900 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2 items-end max-w-4xl mx-auto">
          {messages.length > 0 && (
            <button
              type="button"
              onClick={onClear}
              className="flex-shrink-0 p-2.5 rounded-xl text-dark-400 hover:text-dark-200 hover:bg-dark-800 transition-colors"
              title="Clear chat"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}

          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={handleTextareaInput}
              onKeyDown={handleKeyDown}
              placeholder="Ask about mattresses..."
              rows={1}
              className="w-full resize-none bg-dark-800 border border-dark-600 rounded-xl px-4 py-3 pr-12 text-sm text-dark-100 placeholder-dark-500 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500/50 transition-all"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 bottom-2 p-1.5 rounded-lg bg-primary-600 text-white hover:bg-primary-500 disabled:opacity-40 disabled:hover:bg-primary-600 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </form>

        <p className="text-center text-[10px] text-dark-600 mt-2">
          MattressAI uses RAG with local LLM (DeepSeek via Ollama). Answers are based on ingested PDF documents.
        </p>
      </div>
    </div>
  );
}
