import ReactMarkdown from 'react-markdown';
import { Message } from '../types';
import SourceCard from './SourceCard';

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] lg:max-w-[75%] ${isUser ? 'order-1' : 'order-1'}`}>
        {/* Avatar + Name */}
        <div className={`flex items-center gap-2 mb-1 ${isUser ? 'justify-end' : 'justify-start'}`}>
          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
            isUser ? 'bg-primary-600 text-white' : 'bg-dark-600 text-primary-400'
          }`}>
            {isUser ? 'U' : 'AI'}
          </div>
          <span className="text-xs text-dark-400">
            {isUser ? 'You' : 'MattressAI'}
          </span>
        </div>

        {/* Message Content */}
        <div className={`rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-primary-600 text-white rounded-tr-sm'
            : 'bg-dark-800 text-dark-100 rounded-tl-sm border border-dark-700'
        }`}>
          {isUser ? (
            <p className="text-sm leading-relaxed">{message.content}</p>
          ) : (
            <div className={`message-content text-sm ${message.isStreaming && !message.content ? 'typing-cursor' : ''}`}>
              {message.content ? (
                <ReactMarkdown>{message.content}</ReactMarkdown>
              ) : (
                <div className="flex items-center gap-2 text-dark-400">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 rounded-full bg-primary-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 rounded-full bg-primary-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 rounded-full bg-primary-500 animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                  <span className="text-xs">Thinking...</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Source Citations */}
        {!isUser && message.sources && message.sources.length > 0 && !message.isStreaming && (
          <div className="mt-2 space-y-1">
            <p className="text-xs text-dark-400 font-medium ml-1">Sources Referenced:</p>
            {message.sources.map((source, idx) => (
              <SourceCard key={idx} source={source} index={idx} />
            ))}
          </div>
        )}

        {/* Timestamp */}
        <p className={`text-[10px] text-dark-500 mt-1 ${isUser ? 'text-right' : 'text-left'} ml-1`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
}
