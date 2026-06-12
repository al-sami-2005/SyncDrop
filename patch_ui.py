import re

with open('index.html', 'r') as f:
    html = f.read()

# We want to replace everything from `<style>` at line 351 to `<div id="legacy-ui">`
start_marker = "<style>\n:root {\n  --primary: #3B82F6;"
end_marker = "<div id=\"legacy-ui\">"

new_ui = """<style>
:root {
  --primary: #6366F1;
  --primary-glow: rgba(99, 102, 241, 0.4);
  --secondary: #8B5CF6;
  --bg-app: #0a0a0f;
  --card-bg: rgba(255, 255, 255, 0.03);
  --card-border: rgba(255, 255, 255, 0.08);
  --text-main: #F8FAFC;
  --text-muted: #94A3B8;
  --success: #10B981;
  --danger: #EF4444;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg-app);
  color: var(--text-main);
  font-family: var(--font-sans);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

/* Animated Mesh Background */
.bg-mesh {
  position: absolute;
  top: -50%; left: -50%; width: 200%; height: 200%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.1) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.1) 0%, transparent 40%);
  z-index: -1;
  animation: meshFloat 20s infinite linear alternate;
}
@keyframes meshFloat {
  0% { transform: scale(1) rotate(0deg); }
  100% { transform: scale(1.2) rotate(15deg); }
}

/* App Container (Full screen on mobile, centered card on desktop) */
.app-container {
  width: 100%;
  max-width: 520px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  overflow-y: auto;
  position: relative;
}
@media (min-width: 768px) {
  .app-container {
    height: 90vh;
    border: 1px solid var(--card-border);
    border-radius: 32px;
    box-shadow: var(--glass-shadow);
  }
}

.app-content {
  flex: 1;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.app-title {
  font-size: 28px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}
.app-header .material-icons-round {
  color: var(--text-muted);
  font-size: 28px;
  cursor: pointer;
  transition: 0.3s;
}
.app-header .material-icons-round:hover {
  color: var(--text-main);
  transform: rotate(45deg);
}

/* Connection Card */
.conn-card {
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15));
  border: 1px solid rgba(139,92,246,0.3);
  border-radius: 24px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(99,102,241,0.1);
  transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.conn-card:hover { border-color: rgba(139,92,246,0.6); box-shadow: 0 15px 40px rgba(99,102,241,0.2); }
.conn-header { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.conn-icon {
  width: 48px; height: 48px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 20px var(--primary-glow);
}
.conn-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.conn-status { font-size: 14px; color: var(--text-muted); display: flex; align-items: center; gap: 8px; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; box-shadow: 0 0 10px currentColor; }

/* Code & QR */
.code-display {
  display: flex; align-items: center; justify-content: space-between;
  background: rgba(0,0,0,0.4); padding: 16px 20px; border-radius: 16px; border: 1px solid var(--card-border);
  margin-bottom: 20px;
}
.code-display span { font-size: 14px; color: var(--text-muted); }
.code-display b { font-size: 24px; letter-spacing: 4px; color: var(--primary); font-family: monospace; }
.qr-container { display: flex; justify-content: center; margin-bottom: 20px; }
.qr-box { background: white; padding: 12px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }

/* Inputs */
.connect-inputs { display: flex; gap: 12px; }
.connect-input {
  flex: 1; background: rgba(0,0,0,0.4); border: 1px solid var(--card-border);
  border-radius: 16px; padding: 16px; color: white; font-size: 18px;
  text-align: center; letter-spacing: 2px; outline: none; transition: 0.3s;
}
.connect-input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(99,102,241,0.2); }
.connect-input::placeholder { color: rgba(255,255,255,0.2); font-size: 16px; letter-spacing: 1px; }

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white; border: none; padding: 0 24px; border-radius: 16px;
  font-size: 16px; font-weight: 600; cursor: pointer; transition: 0.3s;
  box-shadow: 0 8px 20px var(--primary-glow);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 25px var(--primary-glow); }
.btn-primary:active { transform: scale(0.96); }

.btn-danger {
  background: rgba(239, 68, 68, 0.1); color: var(--danger);
  border: 1px solid rgba(239, 68, 68, 0.3); padding: 12px 24px; border-radius: 16px;
  font-size: 15px; font-weight: 600; cursor: pointer; transition: 0.3s;
}
.btn-danger:hover { background: var(--danger); color: white; box-shadow: 0 8px 20px rgba(239, 68, 68, 0.4); }

.conn-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 16px; }
.conn-ip { font-family: monospace; font-size: 15px; color: var(--text-muted); }

/* Quick Actions */
.quick-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
@media (max-width: 380px) { .quick-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; } }
.quick-btn {
  background: rgba(255,255,255,0.03); border: 1px solid var(--card-border);
  border-radius: 20px; padding: 20px 8px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  cursor: pointer; transition: 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.quick-btn:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.15); transform: translateY(-4px); }
.quick-label { font-size: 13px; font-weight: 600; color: var(--text-main); }

/* Storage Card & Transfer Overlay */
.storage-card { background: rgba(0,0,0,0.3); border-radius: 24px; padding: 24px; border: 1px solid var(--card-border); }
.storage-header { display: flex; justify-content: space-between; margin-bottom: 16px; font-size: 15px; font-weight: 600; }
.storage-header span:last-child { color: var(--primary); }
.progress-container { width: 100%; height: 10px; background: rgba(255,255,255,0.05); border-radius: 5px; overflow: hidden; margin-bottom: 16px; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--secondary)); width: 0%; transition: width 0.3s ease; }

/* Transfer Active Overlay */
.transfer-overlay {
  display: none; flex-direction: column; align-items: center; justify-content: center;
  background: rgba(10,10,15,0.95); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: 100;
  padding: 40px; text-align: center; border-radius: inherit;
  animation: fadeIn 0.4s ease forwards;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.transfer-rings {
  position: relative; width: 160px; height: 160px; margin-bottom: 32px;
  display: flex; align-items: center; justify-content: center;
}
.ring {
  position: absolute; border-radius: 50%; border: 2px solid transparent;
}
.ring-1 { width: 160px; height: 160px; border-top-color: var(--primary); animation: orbitalSpin 2s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite; }
.ring-2 { width: 130px; height: 130px; border-right-color: var(--secondary); animation: orbitalSpin 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite reverse; }
.ring-icon { font-size: 48px; color: white; filter: drop-shadow(0 0 15px var(--primary)); animation: pulseGlow 2s infinite alternate; }
@keyframes orbitalSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes pulseGlow { 0% { transform: scale(0.9); opacity: 0.8; } 100% { transform: scale(1.1); opacity: 1; } }
.transfer-title { font-size: 24px; font-weight: bold; margin-bottom: 8px; }
.transfer-meta { font-size: 16px; color: var(--text-muted); margin-bottom: 32px; font-family: monospace; }
.transfer-progress { font-size: 40px; font-weight: 800; color: var(--primary); margin-bottom: 40px; }

/* Recent */
.recent-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.recent-title { font-size: 20px; font-weight: bold; }
.recent-list { display: flex; flex-direction: column; gap: 12px; }
.recent-item {
  background: rgba(0,0,0,0.3); border: 1px solid var(--card-border);
  border-radius: 20px; padding: 16px; display: flex; align-items: center; gap: 16px;
  transition: 0.3s;
}
.recent-item:hover { background: rgba(255,255,255,0.05); }
.recent-icon { width: 48px; height: 48px; background: rgba(255,255,255,0.05); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; color: var(--text-muted); }
.recent-info { flex: 1; }
.recent-name { font-size: 15px; font-weight: 600; margin-bottom: 4px; word-break: break-all; }
.recent-meta { font-size: 13px; color: var(--text-muted); }
.recent-status { color: var(--success); font-size: 24px; }

/* Modals */
.modal-overlay {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.8); backdrop-filter: blur(10px);
  z-index: 999; display: flex; justify-content: center; align-items: center;
  opacity: 0; pointer-events: none; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 24px; border-radius: inherit;
}
.modal-overlay.active { opacity: 1; pointer-events: all; }
.modal-box {
  background: #15151E; border: 1px solid rgba(255,255,255,0.1);
  width: 100%; max-width: 440px; border-radius: 28px; padding: 32px;
  display: flex; flex-direction: column; gap: 20px;
  transform: translateY(40px); transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 25px 50px rgba(0,0,0,0.6);
}
.modal-overlay.active .modal-box { transform: translateY(0); }
.modal-header { display: flex; justify-content: space-between; align-items: center; }
.modal-header h3 { font-size: 20px; font-weight: bold; }
.modal-header .material-icons-round { cursor: pointer; color: var(--text-muted); font-size: 24px; }
.modal-header .material-icons-round:hover { color: white; }
#modern-code-textarea {
  width: 100%; height: 220px; background: rgba(0,0,0,0.5); color: #10B981;
  font-family: monospace; border: 1px solid rgba(255,255,255,0.1); border-radius: 16px;
  padding: 20px; resize: none; outline: none; font-size: 15px; line-height: 1.5;
}
#modern-code-textarea:focus { border-color: var(--primary); }
</style>
</head>
<body data-theme="dark">
<div class="bg-mesh"></div>

<div class="app-container">
  <div class="app-content">
    
    <!-- Header -->
    <div class="app-header">
      <div class="app-title">SyncDrop</div>
      <span class="material-icons-round" id="modern-settings-btn">settings</span>
    </div>

    <!-- Connection Card -->
    <div class="conn-card" id="modern-conn-card">
      <div class="conn-header">
        <div class="conn-icon"><span class="material-icons-round" style="color:white;">devices</span></div>
        <div>
          <div class="conn-title" id="modern-peer-name">Not Connected</div>
          <div class="conn-status">
            <div class="status-dot" id="modern-status-dot" style="background:var(--danger)"></div>
            <span id="modern-status-text">Waiting for connection...</span>
          </div>
        </div>
      </div>
      
      <!-- Disconnected State -->
      <div id="modern-disconnected-state">
        <div class="code-display">
          <span>Your Code</span>
          <b id="modern-my-code">------</b>
        </div>
        <div class="qr-container">
          <div class="qr-box" id="modern-qr-code"></div>
        </div>
        <div class="connect-inputs">
          <input type="text" id="modern-connect-input" class="connect-input" placeholder="ENTER CODE" maxlength="6">
          <button class="btn-primary" id="modern-connect-btn">Connect</button>
        </div>
      </div>

      <!-- Connected State -->
      <div class="conn-footer" id="modern-connected-state" style="display:none;">
        <div class="conn-ip" id="modern-peer-ip">192.168.x.x</div>
        <button class="btn-danger" id="modern-disconnect-btn">Disconnect</button>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-grid">
      <div class="quick-btn" id="modern-btn-photos">
        <span class="material-icons-round" style="font-size:32px; color:#3B82F6;">image</span>
        <div class="quick-label">Photos</div>
      </div>
      <div class="quick-btn" id="modern-btn-files">
        <span class="material-icons-round" style="font-size:32px; color:#10B981;">description</span>
        <div class="quick-label">Files</div>
      </div>
      <div class="quick-btn" id="modern-btn-folders">
        <span class="material-icons-round" style="font-size:32px; color:#F59E0B;">folder</span>
        <div class="quick-label">Folders</div>
      </div>
      <div class="quick-btn" id="modern-btn-clip">
        <span class="material-icons-round" style="font-size:32px; color:#8B5CF6;">code</span>
        <div class="quick-label">Text Share</div>
      </div>
    </div>

    <!-- Storage Card -->
    <div class="storage-card">
      <div class="storage-header">
        <span>Transfer Stats</span>
        <span id="modern-transfer-stats">0 MB of 0 MB</span>
      </div>
      <div class="progress-container" id="modern-progress-fill">
        <div class="progress-fill" id="modern-prog-bar"></div>
      </div>
    </div>

    <!-- Recent Transfers -->
    <div class="recent-header">
      <div class="recent-title">Recent</div>
    </div>
    <div class="recent-list" id="modern-recent-list">
      <!-- Populated by JS -->
      <div class="recent-item" style="opacity: 0.5;">
        <div class="recent-icon"><span class="material-icons-round">history</span></div>
        <div class="recent-info">
          <div class="recent-name">No recent transfers</div>
          <div class="recent-meta">Transfer files to see them here</div>
        </div>
      </div>
    </div>

  </div>

  <!-- Active Transfer Overlay -->
  <div class="transfer-overlay" id="modern-transfer-overlay">
    <div class="transfer-rings">
      <div class="ring ring-1"></div>
      <div class="ring ring-2"></div>
      <span class="material-icons-round ring-icon">sync</span>
    </div>
    <div class="transfer-title" id="modern-transfer-overlay-title">Transferring...</div>
    <div class="transfer-meta" id="modern-transfer-overlay-meta">Connecting</div>
    <div class="transfer-progress" id="modern-transfer-overlay-pct">0%</div>
    <button class="btn-danger" id="modern-cancel-btn" style="padding: 16px 32px; font-size: 16px; border-radius: 20px;">
      <span class="material-icons-round" style="vertical-align: middle; margin-right: 8px;">cancel</span>Cancel Transfer
    </button>
  </div>

  <!-- Settings Modal -->
  <div class="modal-overlay" id="settings-modal-overlay">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Settings</h3>
        <span class="material-icons-round" id="close-settings-modal">close</span>
      </div>
      <div style="font-size: 15px; color: var(--text-muted); line-height: 1.6;">
        <p><b>SyncDrop</b> is a premium peer-to-peer file sharing application. All files are transferred securely via WebRTC DataChannels.</p>
        <br>
        <p>Your Device Code: <span style="color: var(--primary); font-family: monospace;"></span></p>
      </div>
    </div>
  </div>

  <!-- Code Share Modal -->
  <div class="modal-overlay" id="code-modal-overlay">
    <div class="modal-box">
      <div class="modal-header">
        <h3 id="code-modal-title">Share Text / Code</h3>
        <span class="material-icons-round" id="close-code-modal">close</span>
      </div>
      <textarea id="modern-code-textarea" placeholder="Paste your code or text here..."></textarea>
      <button id="modern-send-code-execute" class="btn-primary" style="padding: 16px;">Send Code</button>
    </div>
  </div>

</div>

<script>
// Additional modern hooks for new features
document.addEventListener("DOMContentLoaded", () => {
    // Generate QR Code once the code is available
    const checkCode = setInterval(() => {
        const code = document.getElementById('modern-my-code').innerText;
        if (code && code !== '------') {
            clearInterval(checkCode);
            try {
                new QRCode(document.getElementById("modern-qr-code"), {
                    text: window.location.href.split('?')[0] + '?code=' + code,
                    width: 140,
                    height: 140,
                    colorDark : "#0a0a0f",
                    colorLight : "#ffffff",
                    correctLevel : QRCode.CorrectLevel.L
                });
            } catch(e) {}
        }
    }, 1000);

    // Cancel Button
    document.getElementById('modern-cancel-btn').addEventListener('click', () => {
        if (typeof cancelTransfer === 'function') cancelTransfer();
        document.getElementById('modern-transfer-overlay').style.display = 'none';
    });

    // Settings Modal
    document.getElementById('modern-settings-btn').addEventListener('click', () => {
        document.getElementById('settings-modal-overlay').classList.add('active');
    });
    document.getElementById('close-settings-modal').addEventListener('click', () => {
        document.getElementById('settings-modal-overlay').classList.remove('active');
    });

    // Ensure modern-progress-fill updates inner modern-prog-bar
    const origStats = document.getElementById('modern-progress-fill');
    if(origStats) {
        Object.defineProperty(origStats.style, 'width', {
            set: function(val) {
                const bar = document.getElementById('modern-prog-bar');
                if(bar) bar.style.width = val;
                
                // Show overlay if transfer active
                const overlay = document.getElementById('modern-transfer-overlay');
                if (val !== '100%' && val !== '0%') {
                    if (overlay.style.display !== 'flex') overlay.style.display = 'flex';
                    document.getElementById('modern-transfer-overlay-pct').innerText = val;
                    const stats = document.getElementById('modern-transfer-stats').innerText;
                    document.getElementById('modern-transfer-overlay-meta').innerText = stats;
                } else if (val === '100%') {
                    setTimeout(() => overlay.style.display = 'none', 1000);
                }
            }
        });
    }
});
</script>

"""

idx_start = html.find(start_marker)
idx_end = html.find(end_marker)

if idx_start != -1 and idx_end != -1:
    html = html[:idx_start] + new_ui + html[idx_end:]
    with open('index.html', 'w') as f:
        f.write(html)
    print("UI Replaced Successfully")
else:
    print("Could not find markers")
    print(f"Start: {idx_start}, End: {idx_end}")

