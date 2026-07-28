import { useEffect, useState } from 'react'

const ICONS = {
  hate_speech:   '⚠️',
  harassment:    '🚫',
  cyberbullying: '🛑',
}

export default function AlertBanner({ alert, onDismiss }) {
  const [hiding, setHiding] = useState(false)

  useEffect(() => {
    if (!alert) { setHiding(false); return }
    setHiding(false)
    const t = setTimeout(() => setHiding(true), 3900)
    return () => clearTimeout(t)
  }, [alert])

  if (!alert) return null

  const icon = ICONS[alert.label] || '⚠️'

  return (
    <div className={`alert-banner${hiding ? ' hide' : ''}`}>
      <span className="alert-icon">{icon}</span>
      <div className="alert-body">
        <div className="alert-title">{alert.label_display} Detected</div>
        <div className="alert-sub">Content has been flagged by the AI system.</div>
      </div>
      <button className="alert-close" onClick={onDismiss} aria-label="Dismiss">×</button>
      <div className="alert-bar" />
    </div>
  )
}
