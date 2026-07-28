import { LABEL_META } from '../config'

const CSS_MAP = {
  not_cyberbullying: 'cat-safe',
  hate_speech:       'cat-hate',
  harassment:        'cat-harass',
  cyberbullying:     'cat-cyber',
}

const BADGE_CSS = {
  not_cyberbullying: 'safe',
  hate_speech:       'hate',
  harassment:        'harass',
  cyberbullying:     'cyber',
}

function fmtTime(ts) {
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function Badge({ result }) {
  if (result === null) {
    return (
      <span className="badge pending">
        <span className="analyzing-dots">
          Analyzing<span>.</span><span>.</span><span>.</span>
        </span>
      </span>
    )
  }
  if (result === 'error') {
    return <span className="badge error">⚠ Detection unavailable</span>
  }
  const meta = LABEL_META[result.label] || {}
  const pct  = Math.round(result.confidence * 100)
  const css  = BADGE_CSS[result.label] || 'safe'
  return (
    <span className={`badge ${css}`}>
      {meta.icon} {meta.display} — {pct}%
    </span>
  )
}

export default function Message({ msg }) {
  const { user, avatar, text, isSelf, result, ts } = msg
  const catClass = result && result !== 'error' ? (CSS_MAP[result.label] || '') : ''

  return (
    <div className={`message${isSelf ? ' self' : ''}${catClass ? ` ${catClass}` : ''}`}>
      <div className="avatar">{avatar}</div>
      <div className="msg-body">
        <div className="msg-meta">
          <span className={`msg-user${isSelf ? ' self' : ''}`}>{user}</span>
          <span className="msg-time">{fmtTime(ts)}</span>
        </div>
        <div className="msg-text">{text}</div>
        <div className="msg-badge-wrap">
          <Badge result={result} />
        </div>
      </div>
    </div>
  )
}
