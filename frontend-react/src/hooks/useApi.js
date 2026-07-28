import { useState, useEffect, useCallback, useRef } from 'react'
import { API_BASE } from '../config'

export function useApi() {
  const [apiOnline, setApiOnline] = useState(null) // null = still checking
  const [metrics,   setMetrics  ] = useState(null)
  const didLoad = useRef(false)

  const checkHealth = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/health`, {
        signal: AbortSignal.timeout(3000),
      })
      const ok = res.ok
      setApiOnline(ok)
      return ok
    } catch {
      setApiOnline(false)
      return false
    }
  }, [])

  const loadMetrics = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/metrics`)
      if (res.ok) setMetrics(await res.json())
    } catch {
      /* metrics unavailable */
    }
  }, [])

  const analyzeText = useCallback(async (text, model = 'logistic_regression') => {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, model }),
    })
    if (!res.ok) throw new Error(`API ${res.status}`)
    return res.json()
  }, [])

  // Initial health check + periodic poll
  useEffect(() => {
    if (didLoad.current) return
    didLoad.current = true

    checkHealth().then(ok => { if (ok) loadMetrics() })

    const id = setInterval(() => {
      checkHealth().then(ok => { if (ok && !metrics) loadMetrics() })
    }, 15_000)
    return () => clearInterval(id)
  }, [checkHealth, loadMetrics, metrics])

  return { apiOnline, metrics, analyzeText, loadMetrics }
}
