// One-shot, local-only CSS injection. Node 22+; no downloaded dependencies.
const fs = require('node:fs');
const path = require('node:path');
const STYLE_ID = 'tron-divider-session-test';

function applyStyle(css, remove = false) {
  const existing = document.getElementById('tron-divider-session-test');
  if (remove) {
    existing?.remove();
    return { removed: Boolean(existing) };
  }
  if (!document.querySelector('[data-app-shell-frame]')) throw Error('No Codex app shell found.');
  const targets = document.querySelectorAll('[data-app-shell-main-surface="default"]');
  if (!targets.length) throw Error('No supported main chat surface found. Open a chat first.');
  const style = existing || document.createElement('style');
  style.id = 'tron-divider-session-test';
  style.textContent = css;
  if (!existing) document.head.appendChild(style);
  return { applied: true, mainSurfaces: targets.length, styleCount: document.querySelectorAll('#tron-divider-session-test').length };
}

async function connect(url) {
  const parsed = new URL(url);
  if (parsed.protocol !== 'ws:' || parsed.hostname !== '127.0.0.1' || parsed.port !== '9339') {
    throw Error('Refusing a nonlocal or unexpected debugging endpoint.');
  }
  const socket = new WebSocket(url);
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => { socket.close(); reject(Error('Debug connection timed out.')); }, 3000);
    socket.addEventListener('open', () => { clearTimeout(timer); resolve(); }, { once: true });
    socket.addEventListener('error', () => { clearTimeout(timer); reject(Error('Debug connection failed.')); }, { once: true });
  });
  let id = 0;
  const pending = new Map();
  socket.addEventListener('message', event => {
    const data = JSON.parse(event.data);
    const p = pending.get(data.id);
    if (!p) return;
    clearTimeout(p.timer); pending.delete(data.id);
    data.error ? p.reject(Error(data.error.message)) : p.resolve(data.result);
  });
  const connection = {
    async send(method, params) {
      return new Promise((resolve, reject) => {
        const request = ++id;
        const timer = setTimeout(() => { pending.delete(request); reject(Error('Evaluation timed out.')); }, 3000);
        pending.set(request, { resolve, reject, timer });
        socket.send(JSON.stringify({ id: request, method, params }));
      });
    },
    evaluate(expression) { return connection.send('Runtime.evaluate', { expression, returnByValue: true }); },
    close() { socket.close(); }
  };
  return connection;
}

async function main() {
  const remove = process.argv.includes('--restore');
  const css = fs.readFileSync(path.join(__dirname, 'TRON-dividers.css'), 'utf8');
  const deadline = Date.now() + (remove ? 5000 : 45000);
  let lastError;
  do {
    try {
      const response = await fetch('http://127.0.0.1:9339/json/list', { signal: AbortSignal.timeout(2000) });
      if (!response.ok) throw Error('Debug target lookup failed.');
      const targets = await response.json();
      // Never inject into websites, tools, pets, or unrelated browser tabs.
      const candidates = targets.filter(t => t.type === 'page' && /^app:\/\//.test(t.url) && t.webSocketDebuggerUrl);
      let applied = 0;
      for (const target of candidates) {
        const connection = await connect(target.webSocketDebuggerUrl);
        try {
          const probe = await connection.evaluate('Boolean(document.querySelector("[data-app-shell-frame]"))');
          if (!probe.result?.value) continue;
          const result = await connection.evaluate(`(${applyStyle.toString()})(${JSON.stringify(css)},${remove})`);
          if (result.exceptionDetails) throw Error('The current app layout did not accept the divider test.');
          if (result.result?.value?.applied || result.result?.value?.removed) applied++;
        } finally { connection.close(); }
      }
      if (applied || remove) {
        console.log(JSON.stringify({ mode: remove ? 'restore' : 'apply', windows: applied, residentHelper: false }));
        return;
      }
      throw Error('Waiting for a supported Codex chat window.');
    } catch (error) { lastError = error; }
    await new Promise(resolve => setTimeout(resolve, 1000));
  } while (Date.now() < deadline);
  throw Error(`Could not apply the session style: ${lastError?.message}. No app files were changed.`);
}

module.exports = { applyStyle, STYLE_ID, connect };
if (require.main === module) main().catch(error => { console.error(error.message); process.exitCode = 1; });
