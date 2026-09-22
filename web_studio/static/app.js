let currentMode = "task";
let activeAgent = "teamlead";
let isAutoMode = true;

function toggleAutoMode() {
  isAutoMode = !isAutoMode;
  const btn = document.getElementById("auto-mode-toggle");
  const txt = document.getElementById("auto-mode-text");
  if (isAutoMode) {
    btn.className = "px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-950/60 text-emerald-400 border border-emerald-800/50 hover:bg-emerald-900/60 transition flex items-center gap-1.5";
    btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400"></span><span id="auto-mode-text">⚡ Авто-режим: ВКЛ (Zero-Touch)</span>`;
  } else {
    btn.className = "px-2.5 py-1 rounded-lg text-xs font-medium bg-amber-950/60 text-amber-300 border border-amber-800/50 hover:bg-amber-900/60 transition flex items-center gap-1.5";
    btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span><span id="auto-mode-text">🛠️ Пошаговый: Правки перед кодом</span>`;
  }
}

async function fetchSystemResources() {
  try {
    const res = await fetch('/api/system_resources');
    const data = await res.json();
    document.getElementById('ram-usage').textContent = `${data.process_ram_mb} MB`;
    document.getElementById('cpu-usage').textContent = `${data.system_cpu_pct}%`;
  } catch (e) {
    console.error(e);
  }
}

async function fetchProjects() {
  try {
    const res = await fetch('/api/projects');
    const data = await res.json();
    const container = document.getElementById('projects-list');
    container.innerHTML = data.projects.map(p => `
      <div class="p-2 rounded-lg hover:bg-slate-800/60 text-slate-300 font-medium flex items-center justify-between cursor-pointer transition">
        <span class="truncate"><i class="fa-solid ${p.is_generated_app ? 'fa-cubes text-emerald-400' : 'fa-folder text-indigo-400'} mr-2"></i> ${p.name}</span>
        <span class="text-[10px] text-slate-500">${p.files_count} files</span>
      </div>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

async function fetchAgents() {
  try {
    const res = await fetch('/api/agents');
    const data = await res.json();
    const container = document.getElementById('agents-list');
    container.innerHTML = data.agents.map(a => `
      <div onclick="selectAgent('${a.name}', '${a.role}', '${a.model}', '${a.avatar}')" class="agent-card p-2.5 rounded-xl border border-slate-800/80 bg-[#12192c]/70 cursor-pointer transition">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <span class="text-lg">${a.avatar}</span>
            <div>
              <div class="text-xs font-bold text-white">${a.name}</div>
              <div class="text-[10px] text-slate-400">${a.role}</div>
            </div>
          </div>
          <span class="text-[9px] px-1.5 py-0.5 rounded bg-slate-800 text-indigo-300 border border-slate-700 font-mono">${a.model.replace('antigravity/', '')}</span>
        </div>
      </div>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

function selectAgent(name, role, model, avatar) {
  activeAgent = name;
  document.getElementById('active-agent-name').textContent = name;
  document.getElementById('active-agent-role').textContent = role;
  document.getElementById('active-agent-model').textContent = model;
  document.getElementById('active-agent-avatar').textContent = avatar;
}

function setMode(mode) {
  currentMode = mode;
  const consultBtn = document.getElementById('mode-consult-btn');
  const taskBtn = document.getElementById('mode-task-btn');
  
  if (mode === 'consult') {
    consultBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold bg-cyan-600 text-white border border-cyan-500 transition flex items-center gap-1.5";
    taskBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 hover:bg-indigo-600/30 transition flex items-center gap-1.5";
  } else {
    taskBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold bg-indigo-600 text-white border border-indigo-500 transition flex items-center gap-1.5";
    consultBtn.className = "px-3 py-1 rounded-lg text-xs font-semibold bg-cyan-600/20 text-cyan-300 border border-cyan-500/40 hover:bg-cyan-600/30 transition flex items-center gap-1.5";
  }
}

async function handlePromptSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('prompt-input');
  const prompt = input.value.trim();
  if (!prompt) return;

  const stream = document.getElementById('terminal-stream');
  const statusEl = document.getElementById('exec-status');
  const sendBtn = document.getElementById('send-btn');

  // Append user command card
  const timeStr = new Date().toLocaleTimeString();
  stream.innerHTML += `
    <div class="bg-[#121829] border border-indigo-500/30 rounded-xl p-3.5 space-y-1.5">
      <div class="flex items-center justify-between text-[11px] text-indigo-400 font-bold">
        <span><i class="fa-solid fa-user mr-1.5"></i> User Command [${currentMode.toUpperCase()}]</span>
        <span class="text-slate-500 font-normal">${timeStr}</span>
      </div>
      <p class="text-xs text-white font-sans font-medium">"${escapeHtml(prompt)}"</p>
    </div>
  `;

  // Append thinking / running card
  const runCardId = `run-${Date.now()}`;
  stream.innerHTML += `
    <div id="${runCardId}" class="bg-[#0e1422] border border-slate-800 rounded-xl p-3.5 space-y-2">
      <div class="flex items-center justify-between text-slate-400 text-[11px]">
        <span class="flex items-center gap-1.5 text-amber-300 font-bold">
          <i class="fa-solid fa-circle-notch fa-spin text-xs"></i> 7-Agent Pipeline Executing...
        </span>
        <span class="text-slate-500 text-[10px]">OmniRoute Gateway Active</span>
      </div>
      <div class="bg-[#070a10] p-2.5 rounded-lg border border-slate-900 text-slate-400 font-mono text-[11px] leading-relaxed">
        [Stage 1] Product Manager: Formulating PRD & Gherkin user stories...<br>
        [Stage 2] UI/UX Designer: Synthesizing Design Tokens & Layout Wireframes...<br>
        [Stage 3] Architect: Synthesizing DDL SQL & OpenAPI contracts...
      </div>
    </div>
  `;
  stream.scrollTop = stream.scrollHeight;

  statusEl.textContent = "Pipeline executing...";
  sendBtn.disabled = true;
  input.value = "";

  try {
    const res = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: currentMode, prompt: prompt, auto_mode: isAutoMode })
    });

    const data = await res.json();
    const card = document.getElementById(runCardId);

    if (data.status === 'success') {
      const resData = data.result;
      if (data.mode === 'consult') {
        card.innerHTML = `
          <div class="flex items-center justify-between text-cyan-400 text-[11px] font-bold">
            <span class="flex items-center gap-1.5"><i class="fa-solid fa-lightbulb"></i> Consultation Result [PRD & Architecture]</span>
            <span class="text-emerald-400 text-[10px]"><i class="fa-solid fa-check"></i> Ready for Approval</span>
          </div>
          <div class="bg-[#070a10] p-3 rounded-lg border border-slate-900 text-slate-300 font-sans text-xs space-y-2">
            <div><strong class="text-white">Product:</strong> ${escapeHtml(resData.prd?.product_name || 'App')} — ${escapeHtml(resData.prd?.tagline || '')}</div>
            <div><strong class="text-white">Target:</strong> ${(resData.prd?.target_audience || []).join(', ')}</div>
            <div><strong class="text-white">Theme:</strong> ${resData.design?.design_system?.theme_name || 'Dark Slate'}</div>
            <div><strong class="text-white">ADR Decision:</strong> ${escapeHtml(resData.architecture?.adr?.decision || '')}</div>
            <div class="pt-2 border-t border-slate-800 text-[11px] text-indigo-400">
              💡 Чтобы собрать этот проект в код, переключитесь на <strong>Task Mode</strong> и нажмите отправить!
            </div>
          </div>
        `;
      } else {
        card.innerHTML = `
          <div class="flex items-center justify-between text-emerald-400 text-[11px] font-bold">
            <span class="flex items-center gap-1.5"><i class="fa-solid fa-circle-check"></i> Build Complete [${resData.duration_seconds}s]</span>
            <span class="text-indigo-400 text-[10px]">Verified: True</span>
          </div>
          <div class="bg-[#070a10] p-3 rounded-lg border border-slate-900 text-slate-300 font-sans text-xs space-y-2">
            <div><strong class="text-white">Location:</strong> <code>${resData.target_dir}</code></div>
            <div><strong class="text-white">Self-Healing:</strong> ${resData.self_healing?.status}</div>
            <div class="font-mono text-[11px] text-slate-400 bg-slate-950 p-2 rounded border border-slate-900">
              cd ${resData.target_dir} && ./run.sh
            </div>
          </div>
        `;
        fetchProjects();
      }
    } else {
      card.innerHTML = `<div class="text-red-400">Error: ${data.message || 'Execution failed'}</div>`;
    }
  } catch (err) {
    const card = document.getElementById(runCardId);
    if (card) card.innerHTML = `<div class="text-red-400">Network error: ${err.message}</div>`;
  } finally {
    statusEl.textContent = "Ready for prompt";
    sendBtn.disabled = false;
    stream.scrollTop = stream.scrollHeight;
    fetchSystemResources();
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function refreshData() {
  fetchSystemResources();
  fetchProjects();
  fetchAgents();
}

document.getElementById('prompt-form').addEventListener('submit', handlePromptSubmit);
document.addEventListener('DOMContentLoaded', () => {
  refreshData();
  setInterval(fetchSystemResources, 5000);
});
