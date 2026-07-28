import { useEffect, useRef } from 'react'
import Message      from './Message'
import MessageInput from './MessageInput'
import AlertBanner  from './AlertBanner'

export default function ChatArea({
  messages, onSend, selectedModel, onModelChange, alert, onDismissAlert,
}) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <main className="chat-area">
      <header className="chat-header">
        <div className="ch-info">
          <span className="ch-hash-lg">#</span>
          <span className="ch-name">general</span>
          <span className="ch-desc">AI-monitored space — cyberbullying detection active</span>
        </div>
      </header>

      <AlertBanner alert={alert} onDismiss={onDismissAlert} />

      <div className="messages">
        <div className="day-sep"><span>Today</span></div>

        {messages.map(msg => (
          <Message key={msg.id} msg={msg} />
        ))}

        <div ref={bottomRef} />
      </div>

      <MessageInput
        onSend={onSend}
        selectedModel={selectedModel}
        onModelChange={onModelChange}
      />
    </main>
  )
}
