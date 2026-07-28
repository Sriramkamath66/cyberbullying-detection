import { useState, useEffect, useCallback, useRef } from 'react'
import Sidebar      from './components/Sidebar'
import ChatArea     from './components/ChatArea'
import RightPanel   from './components/RightPanel'
import { useApi }   from './hooks/useApi'
import { DEMO_MESSAGES } from './config'

const INIT_STATS = {
  total: 0, safe: 0, flagged: 0,
  cats: { not_cyberbullying: 0, hate_speech: 0, harassment: 0, cyberbullying: 0 },
}

let _id = 0
const mkMsg = (fields) => ({ id: ++_id, result: null, ts: Date.now(), ...fields })

export default function App() {
  const [messages,      setMessages     ] = useState([])
  const [stats,         setStats        ] = useState(INIT_STATS)
  const [selectedModel, setSelectedModel] = useState('logistic_regression')
  const [alert,         setAlert        ] = useState(null)
  const { apiOnline, metrics, analyzeText } = useApi()
  const alertTimer   = useRef(null)
  const demoLoaded   = useRef(false)

  /* ── Record a detection result into stats + trigger alert ─────── */
  const recordResult = useCallback((result) => {
    setStats(prev => ({
      total:   prev.total + 1,
      safe:    prev.safe   + (result.is_cyberbullying ? 0 : 1),
      flagged: prev.flagged + (result.is_cyberbullying ? 1 : 0),
      cats: {
        ...prev.cats,
        [result.label]: (prev.cats[result.label] || 0) + 1,
      },
    }))
    if (result.is_cyberbullying) {
      setAlert({ label_display: result.label_display, label: result.label })
      clearTimeout(alertTimer.current)
      alertTimer.current = setTimeout(() => setAlert(null), 4200)
    }
  }, [])

  /* ── Analyze text and update message in place ─────────────────── */
  const analyzeMsg = useCallback(async (id, text, model) => {
    try {
      const res = await analyzeText(text, model)
      setMessages(prev => prev.map(m => m.id === id ? { ...m, result: res } : m))
      recordResult(res)
    } catch {
      setMessages(prev => prev.map(m => m.id === id ? { ...m, result: 'error' } : m))
    }
  }, [analyzeText, recordResult])

  /* ── Load demo messages once API state is known ───────────────── */
  useEffect(() => {
    if (apiOnline === null || demoLoaded.current) return
    demoLoaded.current = true

    let cancelled = false
    ;(async () => {
      for (const msg of DEMO_MESSAGES) {
        if (cancelled) break
        const m = mkMsg(msg)
        setMessages(prev => [...prev, m])
        if (apiOnline) analyzeMsg(m.id, m.text, selectedModel)
        await new Promise(r => setTimeout(r, 350))
      }
    })()
    return () => { cancelled = true }
  }, [apiOnline]) // eslint-disable-line

  /* ── Send a new message from the user ────────────────────────── */
  const handleSend = useCallback((text) => {
    const m = mkMsg({ user: 'You', avatar: '🧑', text, isSelf: true })
    setMessages(prev => [...prev, m])
    if (apiOnline) analyzeMsg(m.id, text, selectedModel)
  }, [apiOnline, analyzeMsg, selectedModel])

  return (
    <div className="app">
      <Sidebar apiOnline={apiOnline} />
      <ChatArea
        messages={messages}
        onSend={handleSend}
        selectedModel={selectedModel}
        onModelChange={setSelectedModel}
        alert={alert}
        onDismissAlert={() => { setAlert(null); clearTimeout(alertTimer.current) }}
      />
      <RightPanel stats={stats} metrics={metrics} />
    </div>
  )
}
