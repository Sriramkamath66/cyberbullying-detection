import { useRef, useState } from 'react'

const SEND_ICON = (
  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
  </svg>
)

export default function MessageInput({ onSend, selectedModel, onModelChange, disabled }) {
  const [text, setText] = useState('')
  const taRef = useRef(null)

  function handleInput(e) {
    setText(e.target.value)
    const ta = taRef.current
    ta.style.height = ''
    ta.style.height = Math.min(ta.scrollHeight, 120) + 'px'
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    const trimmed = text.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setText('')
    if (taRef.current) taRef.current.style.height = ''
  }

  return (
    <div className="input-area">
      <div className="model-strip">
        <label>Active model:</label>
        <select value={selectedModel} onChange={e => onModelChange(e.target.value)}>
          <option value="logistic_regression">Logistic Regression</option>
          <option value="random_forest">Random Forest</option>
        </select>
      </div>
      <div className="input-box">
        <textarea
          ref={taRef}
          className="msg-ta"
          value={text}
          rows={1}
          placeholder="Type a message in #general…"
          onChange={handleInput}
          onKeyDown={handleKey}
        />
        <button
          className="send-btn"
          onClick={submit}
          disabled={!text.trim() || disabled}
          title="Send (Enter)"
        >
          {SEND_ICON}
        </button>
      </div>
    </div>
  )
}
