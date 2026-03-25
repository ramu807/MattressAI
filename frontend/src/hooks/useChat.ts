import { useState, useCallback, useRef } from 'react';
import { Message, Source, PipelineStep } from '../types';
import { streamChat, createSession, fetchSession } from '../services/api';

const DEFAULT_STEPS: () => PipelineStep[] = () => [
  { step: 'embedding', label: 'Embed Query', icon: 'embed', status: 'pending' },
  { step: 'retrieval', label: 'Vector DB', icon: 'db', status: 'pending' },
  { step: 'generation', label: 'LLM Generate', icon: 'llm', status: 'pending' },
];

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [pipelineSteps, setPipelineSteps] = useState<PipelineStep[]>([]);
  const [pipelineVisible, setPipelineVisible] = useState(false);
  const [sessionRefresh, setSessionRefresh] = useState(0);
  const abortRef = useRef(false);

  const startNewChat = useCallback(async () => {
    const session = await createSession();
    setCurrentSessionId(session.id);
    setMessages([]);
    setPipelineSteps([]);
    setPipelineVisible(false);
    setSessionRefresh(prev => prev + 1);
  }, []);

  const loadSession = useCallback(async (sessionId: string) => {
    const session = await fetchSession(sessionId);
    setCurrentSessionId(sessionId);
    setMessages(
      session.messages.map(m => ({
        id: m.id,
        role: m.role as 'user' | 'assistant',
        content: m.content,
        sources: m.sources,
        timestamp: new Date(m.timestamp),
        isStreaming: false,
      }))
    );
    setPipelineSteps([]);
    setPipelineVisible(false);
  }, []);

  const sendMessage = useCallback(async (query: string) => {
    if (!query.trim() || isLoading) return;
    abortRef.current = false;

    // Create session on first message if none exists
    let sessionId = currentSessionId;
    if (!sessionId) {
      const session = await createSession();
      sessionId = session.id;
      setCurrentSessionId(sessionId);
    }

    // Add user message
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: query,
      timestamp: new Date(),
    };

    // Create placeholder assistant message
    const assistantMsg: Message = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true,
    };

    setMessages(prev => [...prev, userMsg, assistantMsg]);
    setIsLoading(true);

    // Reset pipeline
    setPipelineSteps(DEFAULT_STEPS());
    setPipelineVisible(true);

    try {
      // Build chat history for context
      const chatHistory = messages
        .filter(m => !m.isStreaming)
        .slice(-6)
        .map(m => ({ role: m.role, content: m.content }));

      let sources: Source[] = [];
      let fullContent = '';

      for await (const event of streamChat(query, chatHistory, sessionId)) {
        if (abortRef.current) break;

        if (event.type === 'step') {
          setPipelineSteps(prev =>
            prev.map(s =>
              s.step === event.data.step
                ? { ...s, status: event.data.status, duration_ms: event.data.duration_ms, detail: event.data }
                : s
            )
          );
        } else if (event.type === 'sources') {
          sources = event.data;
        } else if (event.type === 'token') {
          fullContent += event.data;
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantMsg.id
                ? { ...m, content: fullContent, sources }
                : m
            )
          );
        } else if (event.type === 'done') {
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantMsg.id
                ? { ...m, content: fullContent, sources, isStreaming: false }
                : m
            )
          );
        }
      }

      // Ensure streaming is marked complete
      setMessages(prev =>
        prev.map(m =>
          m.id === assistantMsg.id
            ? { ...m, isStreaming: false }
            : m
        )
      );

      // Trigger session list refresh
      setSessionRefresh(prev => prev + 1);
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : 'An error occurred';
      setMessages(prev =>
        prev.map(m =>
          m.id === assistantMsg.id
            ? { ...m, content: `Error: ${errMsg}`, isStreaming: false }
            : m
        )
      );
    } finally {
      setIsLoading(false);
      // Hide pipeline after a delay
      setTimeout(() => setPipelineVisible(false), 5000);
    }
  }, [messages, isLoading, currentSessionId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setCurrentSessionId(null);
    setPipelineSteps([]);
    setPipelineVisible(false);
  }, []);

  return {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
    currentSessionId,
    startNewChat,
    loadSession,
    pipelineSteps,
    pipelineVisible,
    sessionRefresh,
  };
}
