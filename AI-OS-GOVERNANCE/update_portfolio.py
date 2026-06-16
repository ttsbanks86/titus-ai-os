from pathlib import Path

paths = [
    Path(r'C:\Users\tbank\Desktop\Live Cowork\PORTFOLIO-SITE\index.html'),
    Path(r'C:\Users\tbank\Desktop\Live Cowork\PORTFOLIO-SITE\public\index.html'),
]

old_stats = '''<div class="about-stats">
        <div class="stat-box"><div class="stat-num">4</div><div class="stat-lbl">Applications</div></div>
        <div class="stat-box"><div class="stat-num">12+</div><div class="stat-lbl">BA Skills</div></div>
        <div class="stat-box"><div class="stat-num">5</div><div class="stat-lbl">AI Systems Built</div></div>
      </div>'''

new_stats = '''<div class="about-stats">
        <div class="stat-box"><div class="stat-num">8+</div><div class="stat-lbl">Systems Shipped</div></div>
        <div class="stat-box"><div class="stat-num">12+</div><div class="stat-lbl">BA Skills</div></div>
        <div class="stat-box"><div class="stat-num">4</div><div class="stat-lbl">Operating Layers</div></div>
      </div>'''

old_css = '''.project-card{padding:20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:.2s}
.project-card:hover{border-color:rgba(124,58,237,0.15);transform:translateY(-1px)}'''

new_css = '''.project-card{padding:20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:.2s;position:relative;overflow:hidden}
.project-card::after{content:'';position:absolute;inset:auto -20% -60% auto;width:160px;height:160px;background:radial-gradient(circle,rgba(124,58,237,.16),transparent 68%);pointer-events:none}
.project-card:hover{border-color:rgba(124,58,237,0.22);transform:translateY(-1px)}
.project-card.featured{grid-column:span 2;background:linear-gradient(135deg,rgba(124,58,237,.14),rgba(15,17,25,1) 48%,rgba(56,189,248,.08));border-color:rgba(167,139,250,.2)}
.project-card.business{border-color:rgba(56,189,248,.14)}
.project-meta{font-size:10px;color:#a78bfa;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;font-weight:700}'''

old_projects = '''<section id="projects">
  <div class="container">
    <div class="section-title">Projects</div>
    <h2 class="section-heading">Systems I've Built</h2>
    <div class="projects-grid">
      <div class="project-card">
        <div class="project-icon">🎤</div>
        <div class="project-name">Whisper My Idea Pro</div>
        <div class="project-desc">Professional AI transcription app. System tray utility with global hotkey recording, floating HUD, auto-paste into active window. 5 modes, vocabulary management, file transcription. Modeled after SuperWhisper.</div>
        <div class="project-tech"><span>Electron</span><span>Python</span><span>faster-whisper</span></div>
      </div>
      <div class="project-card">
        <div class="project-icon">🗣️</div>
        <div class="project-name">NOLA Voice Reader</div>
        <div class="project-desc">Clipboard-monitoring TTS reader. Watches Windows clipboard and reads copied text aloud. Pure PySide6 native desktop app. 5MB standalone EXE with zero external dependencies.</div>
        <div class="project-tech"><span>PySide6</span><span>pyttsx3</span><span>Windows TTS</span></div>
      </div>
      <div class="project-card">
        <div class="project-icon">🤖</div>
        <div class="project-name">PROMPT-MINE</div>
        <div class="project-desc">Prompt Mining &amp; Intelligence Engine. Extracted and codified 7 universal behavioral patterns from leaked system prompts (Claude, ChatGPT, Gemini, Grok). Injected into 15 AI agents.</div>
        <div class="project-tech"><span>System Prompts</span><span>Agent Loops</span></div>
      </div>
      <div class="project-card">
        <div class="project-icon">⚙️</div>
        <div class="project-name">Automation Hub</div>
        <div class="project-desc">PowerShell + Task Scheduler orchestration system. 8 scheduled tasks running daily for morning briefings, job intelligence scans, goldmine crawls, and design inspiration.</div>
        <div class="project-tech"><span>PowerShell</span><span>Task Scheduler</span></div>
      </div>
    </div>
  </div>
</section>'''

new_projects = '''<section id="projects">
  <div class="container">
    <div class="section-title">Selected Systems</div>
    <h2 class="section-heading">AI Operations, Business Workflows &amp; Product Builds</h2>
    <div class="projects-grid">
      <div class="project-card featured">
        <div class="project-meta">New · AI Operating System Visibility</div>
        <div class="project-icon">🧠</div>
        <div class="project-name">Titus AI OS Brain</div>
        <div class="project-desc">Local visual system map that shows how OpenCode, Claude, Goose, agents, skills, projects, workflows, memory notes, portfolio items, and approval-gated risks connect. Built to make a complex multi-agent operating system understandable at a glance.</div>
        <div class="project-tech"><span>Python</span><span>Cytoscape.js</span><span>Knowledge Graph</span><span>Local-First</span></div>
      </div>
      <div class="project-card featured business">
        <div class="project-meta">Business Collaboration · Operations Cockpit</div>
        <div class="project-icon">🧭</div>
        <div class="project-name">Command Center</div>
        <div class="project-desc">Desktop control surface for launching and monitoring local business tools: gateway/bot controls, DocFlow, Pipeline CRM/API, learning captures, and AI OS governance. Rebuilt as a practical operator console rather than a static dashboard.</div>
        <div class="project-tech"><span>Python</span><span>PySide</span><span>Desktop App</span><span>Workflow Ops</span></div>
      </div>
      <div class="project-card">
        <div class="project-meta">Voice-to-Execution Product</div>
        <div class="project-icon">🎤</div>
        <div class="project-name">Whisper My Idea Pro</div>
        <div class="project-desc">Professional AI transcription and idea-capture app with system tray utility, global hotkey recording, floating HUD, auto-paste into active windows, multiple capture modes, vocabulary management, and file transcription.</div>
        <div class="project-tech"><span>Electron</span><span>Python</span><span>faster-whisper</span><span>UX Automation</span></div>
      </div>
      <div class="project-card business">
        <div class="project-meta">Local Voice Utility</div>
        <div class="project-icon">🗣️</div>
        <div class="project-name">NOLA Voice Reader</div>
        <div class="project-desc">Clipboard-monitoring TTS reader that watches copied text and reads it aloud through a clean local desktop workflow. Presented as practical accessibility, productivity, and local-first AI tooling.</div>
        <div class="project-tech"><span>PySide6</span><span>Windows TTS</span><span>Local Utility</span></div>
      </div>
      <div class="project-card business">
        <div class="project-meta">Pipeline &amp; Systems Operations</div>
        <div class="project-icon">📊</div>
        <div class="project-name">DocFlow + Pipeline CRM</div>
        <div class="project-desc">Document workflow and pipeline operations tooling for tracking work, handoffs, automation steps, and business rhythm. Framed around visibility, repeatable process, and reducing operational drift.</div>
        <div class="project-tech"><span>DocFlow</span><span>Pipeline CRM</span><span>Process Mapping</span></div>
      </div>
      <div class="project-card">
        <div class="project-meta">Document Workflow App</div>
        <div class="project-icon">📄</div>
        <div class="project-name">DocFlow</div>
        <div class="project-desc">Local desktop document workflow utility rebuilt and debugged through a production-style loop: trace the crash, patch the narrow issue, rebuild the EXE, verify the shortcut, and save the troubleshooting lesson.</div>
        <div class="project-tech"><span>Python</span><span>PySide</span><span>PyInstaller</span><span>QA</span></div>
      </div>
      <div class="project-card">
        <div class="project-meta">Agent Behavior System</div>
        <div class="project-icon">🤖</div>
        <div class="project-name">PROMPT-MINE</div>
        <div class="project-desc">Prompt Mining &amp; Intelligence Engine. Extracted reusable behavioral patterns from leading AI systems and codified them into practical agent loops, delegation rules, safety gates, and operating procedures.</div>
        <div class="project-tech"><span>System Prompts</span><span>Agent Loops</span><span>Governance</span></div>
      </div>
      <div class="project-card">
        <div class="project-meta">Automation Infrastructure</div>
        <div class="project-icon">⚙️</div>
        <div class="project-name">Automation Hub</div>
        <div class="project-desc">PowerShell and scheduled-task orchestration for daily briefings, job intelligence, learning capture, research scans, and recurring operational workflows.</div>
        <div class="project-tech"><span>PowerShell</span><span>Task Scheduler</span><span>Ops Automation</span></div>
      </div>
    </div>
  </div>
</section>'''

for path in paths:
    text = path.read_text(encoding='utf-8')
    if old_stats not in text:
        raise SystemExit(f'Expected stats block missing in {path}')
    if old_css not in text:
        raise SystemExit(f'Expected CSS block missing in {path}')
    if old_projects not in text:
        raise SystemExit(f'Expected projects block missing in {path}')
    text = text.replace(old_stats, new_stats).replace(old_css, new_css).replace(old_projects, new_projects)
    path.write_text(text, encoding='utf-8')
    print(f'updated {path}')
