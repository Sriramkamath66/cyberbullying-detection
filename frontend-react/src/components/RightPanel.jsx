function MetricCard({ data, isBest }) {
  if (!data) return null
  const accPct  = Math.round(data.accuracy  * 100)
  const precPct = Math.round(data.precision * 100)
  return (
    <div className={`metric-card${isBest ? ' best' : ''}`}>
      <div className="mc-head">
        <span className="mc-name">{data.name}</span>
        {isBest && <span className="mc-best">Best Model</span>}
      </div>

      <div className="mc-row">
        <span className="mc-key">Accuracy</span>
        <span className="mc-val">{accPct}%</span>
      </div>
      <div className="mc-track">
        <div className="mc-fill acc" style={{ width: `${accPct}%` }} />
      </div>

      <div className="mc-row">
        <span className="mc-key">Precision</span>
        <span className="mc-val">{precPct}%</span>
      </div>
      <div className="mc-track">
        <div className="mc-fill prec" style={{ width: `${precPct}%` }} />
      </div>
    </div>
  )
}

export default function RightPanel({ stats, metrics }) {
  const flagRate = stats.total
    ? Math.round((stats.flagged / stats.total) * 100) + '%'
    : '0%'

  return (
    <aside className="panel">
      {/* ── Stats ───────────────────────────────── */}
      <div className="panel-sec">
        <p className="panel-label">Detection Stats</p>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-val">{stats.total}</div>
            <div className="stat-lbl">Total</div>
          </div>
          <div className="stat-card s-safe">
            <div className="stat-val" style={{ color: 'var(--safe)' }}>{stats.safe}</div>
            <div className="stat-lbl">Safe</div>
          </div>
          <div className="stat-card s-flag">
            <div className="stat-val" style={{ color: 'var(--harass)' }}>{stats.flagged}</div>
            <div className="stat-lbl">Flagged</div>
          </div>
          <div className="stat-card">
            <div className="stat-val">{flagRate}</div>
            <div className="stat-lbl">Flag Rate</div>
          </div>
        </div>
      </div>

      {/* ── Model comparison ────────────────────── */}
      <div className="panel-sec">
        <p className="panel-label">Model Comparison</p>
        {metrics ? (
          <>
            <MetricCard
              data={metrics.logistic_regression}
              isBest={metrics.best_model === 'logistic_regression'}
            />
            <MetricCard
              data={metrics.random_forest}
              isBest={metrics.best_model === 'random_forest'}
            />
          </>
        ) : (
          <p className="no-metrics">
            Run <code>train.py</code> then start the API server to see model metrics here.
          </p>
        )}
      </div>

      {/* ── Category breakdown ──────────────────── */}
      <div className="panel-sec">
        <p className="panel-label">Category Breakdown</p>
        <div className="cat-list">
          <div className="cat-row">
            <span className="cat-dot cd-safe" />
            <span className="cat-name">Safe</span>
            <span className="cat-cnt">{stats.cats.not_cyberbullying}</span>
          </div>
          <div className="cat-row">
            <span className="cat-dot cd-hate" />
            <span className="cat-name">Hate Speech</span>
            <span className="cat-cnt">{stats.cats.hate_speech}</span>
          </div>
          <div className="cat-row">
            <span className="cat-dot cd-harass" />
            <span className="cat-name">Harassment</span>
            <span className="cat-cnt">{stats.cats.harassment}</span>
          </div>
          <div className="cat-row">
            <span className="cat-dot cd-cyber" />
            <span className="cat-name">Cyberbullying</span>
            <span className="cat-cnt">{stats.cats.cyberbullying}</span>
          </div>
        </div>
      </div>

      {/* ── Legend ──────────────────────────────── */}
      <div className="panel-sec">
        <p className="panel-label">Legend</p>
        <div className="legend">
          <div className="leg-row"><span className="leg-bar lb-safe" /> Not Cyberbullying</div>
          <div className="leg-row"><span className="leg-bar lb-hate" /> Hate Speech</div>
          <div className="leg-row"><span className="leg-bar lb-harass" /> Harassment</div>
          <div className="leg-row"><span className="leg-bar lb-cyber" /> Cyberbullying</div>
        </div>
      </div>
    </aside>
  )
}
