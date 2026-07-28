// ── Configuration ──────────────────────────────────────────────────────────
const API = 'http://localhost:8000';

// ── State ──────────────────────────────────────────────────────────────────
const state = {
  total: 0,
  safe: 0,
  flagged: 0,
  cats: { not_cyberbullying: 0, hate_speech: 0, harassment: 0, cyberbullying: 0 },
};

// ── Demo pre-seeded messages ────────────────────────────────────────────────
const DEMO_MESSAGES = [
  { user: 'Alice',  avatar: '👩',    text: "Hey everyone! How was the long weekend?" },
  { user: 'Bob',    avatar: '👨',    text: "Pretty good! Went hiking and it was incredible." },
  { user: 'Carol',  avatar: '👩‍💻', text: "I just finished the assignment, finally!" },
  { user: 'Alice',  avatar: '👩',    text: "Congrats Carol! You totally deserve to celebrate." },
  { user: 'Bob',    avatar: '👨',    text: "You are so ugly and nobody in this class actually likes you." },
  { user: 'Carol',  avatar: '👩‍💻', text: "People from that country are all criminals and should be deported." },
  { user: 'Alice',  avatar: '👩',    text: "Do what I say or I will send those screenshots to everyone in school." },
  { user: 'Bob',    avatar: '👨',    text: "Looking forward to the study group on Thursday, see you all there!" },
  { user: 'Carol',  avatar: '👩‍💻', text: "I am going to make your life absolutely miserable from now on." },
  { user: 'Alice',  avatar: '👩',    text: "Has anyone seen the new movie? It is supposed to be amazing!" },
];

// ── API helpers ─────────────────────────────────────────────────────────────
async function checkHealth() {
  try {
    const res = await fetch(`${API}/health`, { signal: AbortSignal.timeout(3000) });
    return res.ok;
  } catch {
    return false;
  }
}

async function analyzeText(text, model = 'logistic_regression') {
  const res = await fetch(`${API}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, model }),
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

async function fetchMetrics() {
  const res = await fetch(`${API}/metrics`);
  if (!res.ok) throw new Error('Metrics unavailable');
  return res.json();
}

// ── Badge helpers ───────────────────────────────────────────────────────────
function labelClass(label) {
  const map = {
    not_cyberbullying: 'safe',
    hate_speech:       'hate',
    harassment:        'harassment',
    cyberbullying:     'cyberbullying',
  };
  return map[label] || 'safe';
}

function msgCatClass(label) {
  const map = {
    not_cyberbullying: 'cat-safe',
    hate_speech:       'cat-hate',
    harassment:        'cat-harassment',
    cyberbullying:     'cat-cyberbullying',
  };
  return map[label] || '';
}

const ICONS = {
  not_cyberbullying: '✅',
  hate_speech:       '⚠️',
  harassment:        '🚫',
  cyberbullying:     '🛑',
};

// ── Render a single message ─────────────────────────────────────────────────
function renderMessage({ user, avatar, text, isSelf = false, result = null }) {
  const messages = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'message' + (isSelf ? ' self' : '');

  const now = new Date();
  const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const badgeHtml = result === null
    ? `<span class="badge analyzing">⏳ Analyzing…</span>`
    : buildBadge(result);

  div.innerHTML = `
    <div class="avatar">${avatar}</div>
    <div class="msg-body">
      <div class="msg-meta">
        <span class="msg-username${isSelf ? ' self-name' : ''}">${escHtml(user)}</span>
        <span class="msg-time">${time}</span>
      </div>
      <div class="msg-text">${escHtml(text)}</div>
      <div class="msg-badge">${badgeHtml}</div>
    </div>
  `;

  if (result) applyCategory(div, result.label);
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

function buildBadge(result) {
  const cls  = labelClass(result.label);
  const icon = ICONS[result.label] || '';
  const pct  = Math.round(result.confidence * 100);
  return `<span class="badge ${cls}">${icon} ${result.label_display} — ${pct}%</span>`;
}

function applyCategory(div, label) {
  div.classList.remove('cat-safe', 'cat-hate', 'cat-harassment', 'cat-cyberbullying');
  const cls = msgCatClass(label);
  if (cls) div.classList.add(cls);
}

function escHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Update stats ────────────────────────────────────────────────────────────
function updateStats(result) {
  state.total++;
  if (result.is_cyberbullying) {
    state.flagged++;
  } else {
    state.safe++;
  }
  state.cats[result.label] = (state.cats[result.label] || 0) + 1;

  document.getElementById('stat-total').textContent   = state.total;
  document.getElementById('stat-safe').textContent    = state.safe;
  document.getElementById('stat-flagged').textContent = state.flagged;
  const rate = state.total ? Math.round((state.flagged / state.total) * 100) : 0;
  document.getElementById('stat-rate').textContent    = rate + '%';

  document.getElementById('cat-safe').textContent   = state.cats.not_cyberbullying || 0;
  document.getElementById('cat-hate').textContent   = state.cats.hate_speech       || 0;
  document.getElementById('cat-harass').textContent = state.cats.harassment        || 0;
  document.getElementById('cat-cyber').textContent  = state.cats.cyberbullying     || 0;
}

// ── Alert banner ─────────────────────────────────────────────────────────────
let alertTimer;
function showAlert(label_display) {
  const banner = document.getElementById('alert-banner');
  const text   = document.getElementById('alert-text');
  banner.classList.remove('hidden');
  text.textContent = `${label_display} detected — content flagged`;
  clearTimeout(alertTimer);
  alertTimer = setTimeout(() => banner.classList.add('hidden'), 4000);
}

// ── Render model metrics ─────────────────────────────────────────────────────
function renderMetrics(data) {
  const container = document.getElementById('metrics-container');
  if (!data || !data.logistic_regression) {
    container.innerHTML = '<div class="metrics-loading">Run train.py to see metrics.</div>';
    return;
  }
  const best = data.best_model;

  function card(key, m) {
    const isBest = key === best;
    const accPct = Math.round(m.accuracy  * 100);
    const prePct = Math.round(m.precision * 100);
    return `
      <div class="model-card${isBest ? ' best' : ''}">
        <div class="model-card-header">
          <span class="model-card-name">${m.name}</span>
          ${isBest ? '<span class="best-badge">Best Model</span>' : ''}
        </div>
        <div class="metric-row">
          <span class="metric-label">Accuracy</span>
          <span class="metric-value">${accPct}%</span>
        </div>
        <div class="metric-bar-bg">
          <div class="metric-bar-fill" style="width:${accPct}%"></div>
        </div>
        <div class="metric-row" style="margin-top:6px">
          <span class="metric-label">Precision</span>
          <span class="metric-value">${prePct}%</span>
        </div>
        <div class="metric-bar-bg">
          <div class="metric-bar-fill" style="width:${prePct}%; background: #3fb950"></div>
        </div>
      </div>`;
  }

  container.innerHTML =
    card('logistic_regression', data.logistic_regression) +
    card('random_forest',       data.random_forest);
}

// ── Send a message ──────────────────────────────────────────────────────────
async function sendMessage() {
  const input = document.getElementById('msg-input');
  const model = document.getElementById('model-select').value;
  const text  = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = '';

  const div = renderMessage({ user: 'You', avatar: '🧑', text, isSelf: true });

  try {
    const result = await analyzeText(text, model);
    const badge  = div.querySelector('.msg-badge');
    badge.innerHTML = buildBadge(result);
    applyCategory(div, result.label);
    updateStats(result);
    if (result.is_cyberbullying) showAlert(result.label_display);
  } catch {
    const badge = div.querySelector('.msg-badge');
    badge.innerHTML = '<span class="badge analyzing">⚠️ Detection unavailable</span>';
  }
}

// ── Load demo messages ───────────────────────────────────────────────────────
async function loadDemoMessages() {
  const model = document.getElementById('model-select').value;

  for (const msg of DEMO_MESSAGES) {
    await new Promise(r => setTimeout(r, 280));
    const div = renderMessage({ ...msg });

    try {
      const result = await analyzeText(msg.text, model);
      const badge = div.querySelector('.msg-badge');
      badge.innerHTML = buildBadge(result);
      applyCategory(div, result.label);
      updateStats(result);
    } catch {
      const badge = div.querySelector('.msg-badge');
      badge.innerHTML = '<span class="badge analyzing">⚠️ API offline</span>';
    }
  }
}

// ── API status check ─────────────────────────────────────────────────────────
async function pollApiStatus() {
  const el   = document.getElementById('api-status');
  const text = document.getElementById('api-status-text');
  const ok   = await checkHealth();

  el.classList.remove('checking', 'online', 'offline');
  if (ok) {
    el.classList.add('online');
    text.textContent = 'API Online';
  } else {
    el.classList.add('offline');
    text.textContent = 'API Offline';
  }
  return ok;
}

// ── Event listeners ─────────────────────────────────────────────────────────
document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('msg-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Auto-resize textarea
document.getElementById('msg-input').addEventListener('input', function () {
  this.style.height = '';
  this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// ── Initialise ───────────────────────────────────────────────────────────────
(async () => {
  const apiOnline = await pollApiStatus();
  setInterval(pollApiStatus, 15000);

  if (apiOnline) {
    try {
      const metrics = await fetchMetrics();
      renderMetrics(metrics);
    } catch {
      renderMetrics(null);
    }
    await loadDemoMessages();
  } else {
    renderMetrics(null);
    // Still render demo messages without badges
    for (const msg of DEMO_MESSAGES) {
      await new Promise(r => setTimeout(r, 180));
      renderMessage({ ...msg });
    }
  }
})();
