import { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { useChat } from './hooks/useChat';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const {
    messages, isLoading, sendMessage, clearMessages,
    currentSessionId, startNewChat, loadSession,
    pipelineSteps, pipelineVisible, sessionRefresh,
  } = useChat();

  return (
    <div className="h-full flex flex-col bg-dark-950 text-dark-100">
      <Header
        onToggleSidebar={() => setSidebarOpen(prev => !prev)}
        sidebarOpen={sidebarOpen}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          currentSessionId={currentSessionId}
          onSelectSession={loadSession}
          onNewChat={startNewChat}
          sessionRefresh={sessionRefresh}
        />

        <main className="flex-1 flex flex-col min-w-0">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            onSendMessage={sendMessage}
            onClear={clearMessages}
            pipelineSteps={pipelineSteps}
            pipelineVisible={pipelineVisible}
          />
        </main>
      </div>
    </div>
  );
}
