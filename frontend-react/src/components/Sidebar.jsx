export default function Sidebar({ apiOnline }) {
  const channels = [
    { name: 'general',       active: true  },
    { name: 'random',        active: false },
    { name: 'support',       active: false },
    { name: 'announcements', active: false },
  ]
  const users = [
    { name: 'Alice',  emoji: '👩'    },
    { name: 'Bob',    emoji: '👨'    },
    { name: 'Carol',  emoji: '👩‍💻' },
    { name: 'You',    emoji: '🧑'    },
  ]

  const statusClass =
    apiOnline === null ? 'check' : apiOnline ? 'online' : 'offline'
  const statusText  =
    apiOnline === null ? 'Checking…' : apiOnline ? 'API Online' : 'API Offline'

  return (
    <aside className="sidebar">
      <div className="sb-header">
        <div className="logo">
          <span className="logo-icon">🛡️</span>
          <span>CyberSafe Chat</span>
        </div>
      </div>

      <p className="sb-label">Channels</p>
      <nav>
        {channels.map(c => (
          <a key={c.name} href="#" className={`channel${c.active ? ' active' : ''}`}>
            <span className="ch-hash">#</span>
            {c.name}
          </a>
        ))}
      </nav>

      <p className="sb-label">Online — {users.length}</p>
      <div className="user-list">
        {users.map(u => (
          <div key={u.name} className="user-row">
            <span className="dot online" />
            {u.emoji} {u.name}
          </div>
        ))}
      </div>

      <div className="api-status-box">
        <p className="sb-label">API Status</p>
        <div className={`api-row ${statusClass}`}>
          <span className={`dot ${statusClass === 'online' ? 'api-on' : statusClass === 'offline' ? 'api-off' : 'check'}`} />
          {statusText}
        </div>
      </div>
    </aside>
  )
}
