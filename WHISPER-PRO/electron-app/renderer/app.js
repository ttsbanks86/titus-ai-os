const API = 'http://127.0.0.1:18927';
let currentPage = 'home';
let isRecording = false;
let mediaRecorder = null;
let stream = null;
let chunks = [];
let timerInterval = null;
let seconds = 0;

// ─── Navigation ──────────────────────────────────────────────────────────
function navigate(page) {
  currentPage = page;
  document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n.dataset.page === page));
  renderPage(page);
}

async function renderPage(page) {
  const c = document.getElementById('content');
  const pages = {
    home: renderHome,
    modes: renderModes,
    vocabulary: renderVocabulary,
    history: renderHistory,
    models: renderModels,
    settings: renderSettings,
    about: renderAbout
  };
  c.innerHTML = `<div class="page active">${await pages[page]()}</div>`;
  if (page === 'home') attachHomeEvents();
  if (page === 'vocabulary') attachVocabEvents();
}

// ─── Home Page ───────────────────────────────────────────────────────────
async function renderHome() {
  let stats = { session_words: 0, total_words: 0, sessions: 0 };
  try {
    const r = await fetch(`${API}/status`);
    const d = await r.json();
    stats = d.stats || stats;
  } catch(e) {}

  return `
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-num">${stats.session_words || 0}</div><div class="stat-lbl">Words This Session</div></div>
      <div class="stat-card"><div class="stat-num">${stats.total_words || 0}</div><div class="stat-lbl">Total Words</div></div>
      <div class="stat-card"><div class="stat-num">${stats.sessions || 0}</div><div class="stat-lbl">Sessions</div></div>
      <div class="stat-card"><div class="stat-num" id="timerDisplay">0:00</div><div class="stat-lbl">Recording Time</div></div>
    </div>
    <div class="record-section">
      <div class="record-timer" id="recTimer">0:00</div>
      <button class="record-btn" id="recBtn" onclick="toggleRecording()">🎤</button>
      <div class="record-label" id="recLabel">Click to record · Alt+Space</div>
    </div>
    <div class="text-card">
      <textarea id="output" placeholder="Transcription will appear here..." readonly></textarea>
      <div style="display:flex;gap:6px;margin-top:8px">
        <button class="btn btn-sm" onclick="copyText()">📋 Copy</button>
        <button class="btn btn-sm" onclick="clearText()">🗑 Clear</button>
      </div>
    </div>
  `;
}

function attachHomeEvents() {
  // Timer display already updates via the recording function
}

// ─── Modes Page ──────────────────────────────────────────────────────────
async function renderModes() {
  const modes = [
    { id: 'Voice', icon: '🎤', label: 'General', desc: 'Standard transcription' },
    { id: 'Message', icon: '💬', label: 'Message', desc: 'Clean message format' },
    { id: 'Email', icon: '✉️', label: 'Email', desc: 'Formatted for email' },
    { id: 'Meeting', icon: '📋', label: 'Meeting', desc: 'Meeting notes' },
    { id: 'Bullets', icon: '📑', label: 'Bullets', desc: 'Bullet point list' },
    { id: 'Custom', icon: '🔧', label: 'Custom', desc: 'Your own format' }
  ];
  return `
    <div class="card">
      <div class="card-title">Recording Modes</div>
      <div class="mode-grid">
        ${modes.map(m => `
          <div class="mode-card" onclick="selectMode('${m.id}')">
            <span class="moji">${m.icon}</span>
            <div style="font-weight:600;margin-bottom:2px">${m.label}</div>
            <div style="font-size:8px;color:#4a5568">${m.desc}</div>
          </div>
        `).join('')}
      </div>
    </div>
    <div class="card">
      <div class="card-title">Custom Mode Builder</div>
      <div style="display:flex;flex-direction:column;gap:8px">
        <input class="vocab-input" placeholder="Mode name..." style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:8px 10px;color:#f0f2f5;font-family:inherit;font-size:11px;outline:none">
        <textarea placeholder="Custom instructions for transcription..." style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:10px;color:#f0f2f5;font-size:11px;font-family:inherit;resize:none;height:60px;outline:none"></textarea>
        <button class="btn btn-sm" style="align-self:flex-start">Save Custom Mode</button>
      </div>
    </div>
  `;
}

function selectMode(mode) {
  document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('active'));
  event.currentTarget.classList.add('active');
}

// ─── Vocabulary Page ─────────────────────────────────────────────────────
async function renderVocabulary() {
  let words = [], phrases = [];
  try {
    const r = await fetch(`${API}/vocabulary`);
    const d = await r.json();
    words = d.words || [];
    phrases = d.phrases || [];
  } catch(e) {}
  return `
    <div class="card">
      <div class="card-title">Vocabulary</div>
      <p style="font-size:10px;color:#6b7280;margin-bottom:10px">Add custom words and phrases to improve transcription accuracy for specialized terms.</p>
      <div class="vocab-input">
        <input type="text" id="vocabInput" placeholder="Add a word or phrase..." onkeypress="if(event.key==='Enter')addWord()">
        <button class="btn btn-sm" onclick="addWord()">+ Add</button>
      </div>
      <div class="vocab-tags" id="vocabTags">
        ${[...words, ...phrases].map(w => `<span class="vocab-tag">${w} <span class="remove" onclick="removeWord('${w}')">✕</span></span>`).join('')}
        ${words.length === 0 && phrases.length === 0 ? '<span style="color:#4a5568;font-size:10px">No vocabulary added yet</span>' : ''}
      </div>
    </div>
  `;
}

function attachVocabEvents() {}

async function addWord() {
  const input = document.getElementById('vocabInput');
  const word = input.value.trim();
  if (!word) return;
  await fetch(`${API}/vocabulary/add`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({word}) });
  input.value = '';
  renderPage('vocabulary');
}

async function removeWord(word) {
  await fetch(`${API}/vocabulary/remove`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({word}) });
  renderPage('vocabulary');
}

// ─── History Page ────────────────────────────────────────────────────────
async function renderHistory() {
  let history = [];
  try {
    const r = await fetch(`${API}/history`);
    history = await r.json();
  } catch(e) {}
  if (history.length === 0) return '<div class="hist-empty">No transcription history yet.<br>Press your hotkey to start recording.</div>';
  return `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <span style="font-size:11px;color:#6b7280">${history.length} entries</span>
      <button class="btn btn-sm" onclick="clearHistory()">🗑 Clear All</button>
    </div>
    <div class="card" style="padding:8px">
      ${history.map((h, i) => `
        <div style="display:flex;align-items:flex-start;gap:6px;padding:8px 4px;border-bottom:1px solid rgba(255,255,255,0.02)">
          <span style="font-size:14px">${getModeIcon(h.mode)}</span>
          <div style="flex:1;min-width:0">
            <div style="font-size:11px;color:#f0f2f5;line-height:1.4">${h.text.substring(0,120)}${h.text.length>120?'...':''}</div>
            <div style="display:flex;gap:8px;margin-top:4px">
              <span style="font-size:9px;color:#4a5568">${h.timestamp || ''}</span>
              <span style="font-size:9px;color:#4a5568">${h.words || 0} words</span>
            </div>
          </div>
          <div style="display:flex;gap:3px;flex-shrink:0">
            <button class="btn btn-sm" onclick="copyHistoryItem('${h.text.replace(/'/g, "\\'").replace(/"/g, '&quot;')}')" title="Copy">📋</button>
            <button class="btn btn-sm" onclick="deleteHistoryItem(${i})" title="Delete">🗑</button>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function copyHistoryItem(text) {
  navigator.clipboard.writeText(text);
}

async function deleteHistoryItem(index) {
  try {
    const r = await fetch(`${API}/history`);
    let h = await r.json();
    // Reverse index because history is returned reversed
    const actualIdx = h.length - 1 - index;
    h.splice(actualIdx, 1);
    await fetch(`${API}/history/save`, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({history: h})
    });
    renderPage('history');
  } catch(e) {}
}

// ─── Models Page ─────────────────────────────────────────────────────────
async function renderModels() {
  const models = [
    { id: 'tiny', name: 'Tiny', desc: 'Fastest, ~1GB RAM', size: '75MB' },
    { id: 'base', name: 'Base', desc: 'Balanced speed/accuracy', size: '150MB' },
    { id: 'small', name: 'Small', desc: 'Good accuracy', size: '500MB' },
    { id: 'medium', name: 'Medium', desc: 'High accuracy', size: '1.5GB' }
  ];
  let current = 'tiny';
  try {
    const r = await fetch(`${API}/models`);
    const d = await r.json();
    current = d.current || 'tiny';
  } catch(e) {}
  return `
    <div class="card">
      <div class="card-title">Transcription Models</div>
      ${models.map(m => `
        <div class="model-card">
          <div>
            <div class="model-name">${m.name} ${current === m.id ? '<span class="model-status">● Active</span>' : ''}</div>
            <div class="model-desc">${m.desc} · ${m.size}</div>
          </div>
          <button class="btn btn-sm" onclick="switchModel('${m.id}')" ${current === m.id ? 'style="opacity:0.4"' : ''}>${current === m.id ? 'Active' : 'Switch'}</button>
        </div>
      `).join('')}
    </div>
  `;
}

async function switchModel(size) {
  try {
    await fetch(`${API}/model/switch`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({size}) });
    renderPage('models');
  } catch(e) {}
}

// ─── Settings Page ───────────────────────────────────────────────────────
async function renderSettings() {
  let s = { hotkey: 'Ctrl+Shift+Space', mode: 'Voice', mic: 'Default', autoPaste: true, saveHistory: true, launchAtStartup: false };
  try { s = await electronAPI.getSettings(); } catch(e) {}
  const hotkeys = [
    'Ctrl+Shift+Space', 'Alt+Space', 'Ctrl+Space', 'Alt+Q', 'Alt+`', 'Alt+X',
    'Ctrl+Alt+Space', 'Ctrl+Shift+R', 'Alt+Shift+R', 'Win+Shift+R', 'Ctrl+Shift+Q',
    'Mouse middle', 'Mouse left', 'Mouse right'
  ];
  return `
    <div class="card">
      <div class="card-title">Hotkey</div>
      <div class="setting-row">
        <div><div class="setting-label">Global Recording Hotkey</div><div class="setting-desc">Press to start/stop recording from any app</div></div>
        <div class="setting-input" style="display:flex;gap:4px;align-items:center">
          <select id="hotkeySelect" onchange="changeHotkey(this.value)" style="background:rgba(0,0,0,0.3);color:#f0f2f5;border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:5px 8px;font-size:10px;font-family:inherit;outline:none;min-width:140px">
            ${hotkeys.map(h => `<option value="${h}" ${h === s.hotkey ? 'selected' : ''}>${h}</option>`).join('')}
          </select>
          <button class="btn btn-sm" onclick="captureHotkey()">🔍 Capture</button>
        </div>
      </div>
      <div id="captureStatus" style="font-size:10px;color:#a78bfa;padding:4px 0;display:none">Press any key or mouse button...</div>
    </div>
    <div class="card">
      <div class="card-title">General</div>
      <div class="setting-row">
        <div><div class="setting-label">Default Mode</div><div class="setting-desc">Transcription mode for new recordings</div></div>
        <div class="setting-input">
          <select id="modeSelect" onchange="saveNamedSetting('mode',this.value)" style="background:rgba(0,0,0,0.3);color:#f0f2f5;border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:5px 8px;font-size:10px;font-family:inherit;outline:none">
            <option value="Voice" ${s.mode==='Voice'?'selected':''}>Voice</option>
            <option value="Message" ${s.mode==='Message'?'selected':''}>Message</option>
            <option value="Email" ${s.mode==='Email'?'selected':''}>Email</option>
            <option value="Meeting" ${s.mode==='Meeting'?'selected':''}>Meeting</option>
            <option value="Bullets" ${s.mode==='Bullets'?'selected':''}>Bullets</option>
          </select>
        </div>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Default Microphone</div><div class="setting-desc">Input device for recording</div></div>
        <div class="setting-input"><span style="font-size:10px;color:#6b7280">System default</span></div>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Auto-paste after recording</div><div class="setting-desc">Type transcription into active window</div></div>
        <div class="setting-input"><input type="checkbox" ${s.autoPaste!==false?'checked':''} onchange="saveNamedSetting('autoPaste',this.checked)" style="accent-color:#6366f1"></div>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Save history</div><div class="setting-desc">Store transcriptions for later reference</div></div>
        <div class="setting-input"><input type="checkbox" ${s.saveHistory!==false?'checked':''} onchange="saveNamedSetting('saveHistory',this.checked)" style="accent-color:#6366f1"></div>
      </div>
      <div class="setting-row">
        <div><div class="setting-label">Launch at Windows startup</div><div class="setting-desc">Auto-start when you log in</div></div>
        <div class="setting-input"><input type="checkbox" ${s.launchAtStartup?'checked':''} onchange="saveNamedSetting('launchAtStartup',this.checked)" style="accent-color:#6366f1"></div>
      </div>
    </div>
  `;
}

async function saveNamedSetting(key, value) {
  try {
    const s = await electronAPI.getSettings();
    s[key] = value;
    await electronAPI.saveSettings(s);
  } catch(e) {}
}

async function changeHotkey(hotkey) {
  try {
    await electronAPI.setHotkey(hotkey);
    await fetch('http://127.0.0.1:18927/set-hotkey', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({hotkey})
    });
    const st = document.getElementById('captureStatus');
    if (st) { st.textContent = `✓ Set to ${hotkey}`; st.style.display = 'block'; st.style.color = '#22c55e'; setTimeout(() => st.style.display = 'none', 2000); }
  } catch(e) {}
}

async function captureHotkey() {
  const st = document.getElementById('captureStatus');
  st.style.display = 'block';
  st.textContent = '⌛ Listening... press any key or mouse button';
  st.style.color = '#a78bfa';
  
  try {
    await fetch('http://127.0.0.1:18927/capture-start', { method: 'POST' });
    
    // Poll for capture result
    let captured = null;
    for (let i = 0; i < 30 && !captured; i++) {
      await new Promise(r => setTimeout(r, 500));
      const res = await fetch('http://127.0.0.1:18927/capture-status');
      const d = await res.json();
      captured = d.key;
    }
    
    if (captured) {
      st.textContent = `✓ Captured: ${captured}`;
      st.style.color = '#22c55e';
      
      // Map common keys to Electron-compatible format
      let mapped = captured;
      if (captured.startsWith('Mouse ')) mapped = captured; // Keep as-is for backend handling
      else if (captured === 'space') mapped = 'Space';
      else if (captured === 'enter') mapped = 'Enter';
      else if (captured === 'tab') mapped = 'Tab';
      else if (captured === 'esc') mapped = 'Escape';
      
      // Update the dropdown
      const sel = document.getElementById('hotkeySelect');
      const opt = document.createElement('option');
      opt.value = mapped; opt.textContent = mapped; opt.selected = true;
      sel.add(opt);
      sel.value = mapped;
      
      // Save
      await changeHotkey(mapped);
    } else {
      st.textContent = '⏱ No key detected. Try again.';
      st.style.color = '#ef4444';
    }
  } catch(e) {
    st.textContent = 'Error connecting to backend';
    st.style.color = '#ef4444';
  }
  
  setTimeout(() => st.style.display = 'none', 3000);
}

// ─── About Page ──────────────────────────────────────────────────────────
function renderAbout() {
  return `
    <div class="card" style="text-align:center;padding:30px">
      <div style="font-size:36px;margin-bottom:8px">🎤</div>
      <div style="font-size:18px;font-weight:700">Whisper My Idea Pro</div>
      <div style="font-size:11px;color:#6b7280;margin-top:4px">Version 2.0 · Built by Titus Banks</div>
      <div style="font-size:10px;color:#4a5568;margin-top:12px">Open Door AI Systems · PROMPT-MINE Engine</div>
      <div style="font-size:10px;color:#4a5568;margin-top:4px">Powered by faster-whisper · PySide6</div>
    </div>
  `;
}

// ─── Recording ───────────────────────────────────────────────────────────
async function toggleRecording() {
  if (isRecording) { stopRecording(); return; }
  isRecording = true;
  const btn = document.getElementById('recBtn');
  btn.className = 'record-btn recording';
  document.getElementById('recLabel').textContent = 'Recording...';
  seconds = 0;
  timerInterval = setInterval(() => {
    seconds++;
    const m = Math.floor(seconds/60), s = seconds%60;
    document.getElementById('recTimer').textContent = `${m}:${s.toString().padStart(2,'0')}`;
  }, 1000);

  try {
    stream = await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,sampleRate:16000}});
    mediaRecorder = new MediaRecorder(stream, {mimeType:'audio/webm'});
    chunks = [];
    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
      clearInterval(timerInterval);
      document.getElementById('recLabel').textContent = 'Transcribing...';
      const blob = new Blob(chunks, {mimeType:'audio/webm'});
      try {
        const r = await fetch(`${API}/transcribe-blob`, {method:'POST',body:blob});
        const d = await r.json();
        document.getElementById('recTimer').textContent = '0:00';
        if (d.text) {
          document.getElementById('output').value = d.text;
          navigator.clipboard.writeText(d.text);
        }
      } catch(e) {
        document.getElementById('output').value = 'Backend unavailable';
      }
      resetRecorder();
    };
    mediaRecorder.start();
  } catch(e) {
    document.getElementById('output').value = 'Microphone access denied';
    resetRecorder();
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    if (stream) stream.getTracks().forEach(t => t.stop());
  }
}

function resetRecorder() {
  isRecording = false;
  const btn = document.getElementById('recBtn');
  if (btn) { btn.className = 'record-btn'; }
  const lbl = document.getElementById('recLabel');
  if (lbl) lbl.textContent = 'Click to record · Alt+Space';
  chunks = [];
  stream = null;
}

function copyText() {
  const t = document.getElementById('output');
  if (t && t.value) { navigator.clipboard.writeText(t.value); }
}

function clearText() {
  const t = document.getElementById('output');
  if (t) t.value = '';
}

// ─── Init ────────────────────────────────────────────────────────────────
electronAPI.onNavigate((page) => navigate(page));
renderPage('home');

// Periodically refresh stats on home page
setInterval(() => {
  if (currentPage === 'home') {
    fetch(`${API}/status`).then(r=>r.json()).then(d => {
      const s = d.stats || {};
      document.querySelectorAll('.stat-num')[0].textContent = s.session_words || 0;
      document.querySelectorAll('.stat-num')[1].textContent = s.total_words || 0;
      document.querySelectorAll('.stat-num')[2].textContent = s.sessions || 0;
    }).catch(()=>{});
  }
}, 3000);
