import base64
import os
import json
import urllib.request
import urllib.error
import sys

# =========================================================================
# SECURE BACKEND KEY FALLBACKS
# =========================================================================
GEMINI_API_KEY = ""
NVIDIA_NIM_KEY = "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"
CUSTOM_API_KEY = ""

if 'streamlit' in sys.modules:
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            if 'GEMINI_API_KEY' in st.secrets:
                GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
            if 'NVIDIA_NIM_KEY' in st.secrets:
                NVIDIA_NIM_KEY = st.secrets['NVIDIA_NIM_KEY']
            if 'CUSTOM_API_KEY' in st.secrets:
                CUSTOM_API_KEY = st.secrets['CUSTOM_API_KEY']
    except Exception:
        pass

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)
NVIDIA_NIM_KEY = os.environ.get("NVIDIA_NIM_KEY", NVIDIA_NIM_KEY)
CUSTOM_API_KEY = os.environ.get("CUSTOM_API_KEY", CUSTOM_API_KEY)

# =========================================================================
# HTML FRONTEND
# =========================================================================
HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAHAY - Government Scheme Finder | సహాయ్ | सहाय | உதவி</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Telugu:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');

  :root {
    --bg: #070b14;
    --surface: #0f172a;
    --surface2: #1e293b;
    --border: #2d3a50;
    --accent: #06b6d4;
    --accent2: #10b981;
    --accent3: #8b5cf6;
    --text: #e2e8f0;
    --text2: #94a3b8;
    --error: #f87171;
    --success: #10b981;
    --warning: #fbbf24;
    --card-radius: 14px;
    --font-main: 'Inter', 'Noto Sans Telugu', 'Noto Sans Devanagari', 'Noto Sans Tamil', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-main);
    min-height: 100vh;
    line-height: 1.6;
  }

  /* HEADER */
  .header {
    background: linear-gradient(135deg, #070b14 0%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
  }

  .logo { display: flex; align-items: center; gap: 12px; }

  .logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
  }

  .logo-text h1 { font-size: 18px; font-weight: 700; color: var(--text); }
  .logo-text p { font-size: 11px; color: var(--text2); letter-spacing: 0.04em; }

  .header-actions { display: flex; gap: 10px; align-items: center; }

  .lang-switcher {
    display: flex; gap: 4px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 4px;
  }

  .lang-btn {
    padding: 5px 11px;
    border: none; border-radius: 7px;
    background: transparent; color: var(--text2);
    font-size: 12px; font-weight: 600;
    cursor: pointer; transition: all 0.2s;
    font-family: var(--font-main);
  }

  .lang-btn.active { background: var(--accent); color: #fff; }
  .lang-btn:hover:not(.active) { background: var(--surface); color: var(--text); }

  .icon-btn {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 8px 14px; border-radius: 10px;
    cursor: pointer; display: flex; align-items: center; gap: 6px;
    font-size: 12.5px; font-family: var(--font-main);
    transition: all 0.2s; font-weight: 600;
  }
  .icon-btn:hover { border-color: var(--accent); color: var(--accent); }

  /* LAYOUT */
  .container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 24px 20px;
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 22px;
  }

  @media (max-width: 900px) { .container { grid-template-columns: 1fr; } }

  /* SIDEBAR */
  .section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 20px;
    margin-bottom: 16px;
  }

  .section-title {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    color: var(--accent2);
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
  }

  .form-group { margin-bottom: 16px; }

  label {
    display: block; font-size: 12px;
    font-weight: 600; color: var(--text2);
    margin-bottom: 7px;
  }

  select, input[type="range"] {
    width: 100%;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    font-family: var(--font-main);
    font-size: 13px;
    padding: 9px 12px;
    outline: none;
    transition: border-color 0.2s;
    -webkit-appearance: none;
  }

  select:focus { border-color: var(--accent); }
  select option { background: var(--surface2); }

  input[type="range"] {
    padding: 0; height: 4px;
    accent-color: var(--accent); cursor: pointer;
  }

  .slider-labels {
    display: flex; justify-content: space-between;
    font-size: 11px; color: var(--text2); margin-top: 6px;
  }

  .budget-display {
    font-size: 17px; font-weight: 700;
    color: var(--accent); margin-top: 4px;
  }

  /* CHIPS */
  .chips { display: flex; flex-wrap: wrap; gap: 7px; }

  .chip {
    padding: 6px 12px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 12px; font-weight: 500;
    color: var(--text2); cursor: pointer;
    transition: all 0.18s;
    background: var(--surface2);
    user-select: none;
    font-family: var(--font-main);
  }

  .chip.selected { background: var(--accent); border-color: var(--accent); color: #fff; }
  .chip:hover:not(.selected) { border-color: var(--accent); color: var(--accent); }

  /* CTA BUTTON */
  .cta-btn {
    width: 100%; padding: 13px 20px;
    background: linear-gradient(135deg, var(--accent), #0891b2);
    border: none; border-radius: 10px;
    color: #fff; font-size: 14px; font-weight: 700;
    cursor: pointer; transition: all 0.2s;
    font-family: var(--font-main);
    display: flex; align-items: center; justify-content: center;
    gap: 8px; letter-spacing: 0.02em;
  }

  .cta-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(6,182,212,0.35); }
  .cta-btn:active { transform: translateY(0); }
  .cta-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }

  /* MAIN CONTENT */
  .hero {
    background: linear-gradient(135deg, var(--surface) 0%, rgba(6,182,212,0.05) 100%);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
  }

  .hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(6,182,212,0.10) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero h2 {
    font-size: 22px; font-weight: 700; margin-bottom: 8px;
    background: linear-gradient(135deg, var(--text), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero p { font-size: 14px; color: var(--text2); line-height: 1.7; }

  .stats-row { display: flex; gap: 24px; margin-top: 20px; flex-wrap: wrap; }
  .stat { display: flex; flex-direction: column; }
  .stat-val { font-size: 22px; font-weight: 800; color: var(--accent); }
  .stat-label { font-size: 11px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.08em; }

  /* TABS */
  .tabs {
    display: flex; gap: 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 18px;
  }

  .tab {
    padding: 10px 18px;
    border: none; background: transparent;
    color: var(--text2); font-size: 13px; font-weight: 600;
    cursor: pointer; border-bottom: 2px solid transparent;
    transition: all 0.2s; font-family: var(--font-main);
    position: relative;
  }

  .tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  .tab:hover:not(.active) { color: var(--text); }

  /* CHAT AREA */
  .chat-area {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    margin-bottom: 16px;
    display: flex; flex-direction: column;
    min-height: 380px; max-height: 560px;
  }

  .chat-header {
    padding: 13px 18px;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }

  .chat-header-left { display: flex; align-items: center; gap: 10px; }

  .ai-status-dot {
    width: 8px; height: 8px;
    border-radius: 50%; background: var(--accent2);
    animation: pulse 2s infinite;
  }

  @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

  .chat-messages {
    flex: 1; overflow-y: auto;
    padding: 18px; display: flex;
    flex-direction: column; gap: 14px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }

  .msg { display: flex; gap: 10px; max-width: 92%; animation: fadeIn 0.3s ease; }

  @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }

  .msg.user { align-self: flex-end; flex-direction: row-reverse; }
  .msg.ai { align-self: flex-start; }

  .msg-avatar {
    width: 32px; height: 32px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
  }

  .msg.ai .msg-avatar { background: linear-gradient(135deg, var(--accent), var(--accent2)); }
  .msg.user .msg-avatar { background: var(--surface2); }

  .msg-bubble {
    padding: 10px 14px; border-radius: 12px;
    font-size: 13.5px; line-height: 1.65;
  }

  .msg.ai .msg-bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-bottom-left-radius: 4px;
  }

  .msg.user .msg-bubble {
    background: var(--accent);
    color: #fff;
    border-bottom-right-radius: 4px;
  }

  /* SCHEME CARDS */
  .scheme-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 16px;
    margin-bottom: 16px;
  }

  .scheme-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    overflow: hidden;
    transition: all 0.2s;
    cursor: pointer;
  }

  .scheme-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
  }

  .scheme-card-header {
    padding: 16px 16px 12px;
    background: linear-gradient(135deg, var(--surface2), rgba(6,182,212,0.05));
    border-bottom: 1px solid var(--border);
    position: relative;
  }

  .scheme-category-badge {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 3px 8px; border-radius: 6px;
    margin-bottom: 8px;
  }

  .cat-health { background: rgba(239,68,68,0.15); color: #f87171; }
  .cat-education { background: rgba(139,92,246,0.15); color: #a78bfa; }
  .cat-agriculture { background: rgba(16,185,129,0.15); color: #6ee7b7; }
  .cat-housing { background: rgba(251,191,36,0.15); color: #fbbf24; }
  .cat-women { background: rgba(236,72,153,0.15); color: #f472b6; }
  .cat-employment { background: rgba(6,182,212,0.15); color: #67e8f9; }
  .cat-pension { background: rgba(99,102,241,0.15); color: #a5b4fc; }

  .scheme-name { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
  .scheme-ministry { font-size: 11px; color: var(--text2); }

  .match-badge {
    position: absolute; top: 12px; right: 12px;
    background: var(--accent2); color: #052e16;
    font-size: 11px; font-weight: 800;
    padding: 3px 9px; border-radius: 10px;
  }

  .scheme-card-body { padding: 14px 16px; }

  .scheme-benefit {
    font-size: 17px; font-weight: 800;
    color: var(--accent); margin-bottom: 8px;
  }

  .scheme-eligibility {
    font-size: 12px; color: var(--text2);
    margin-bottom: 10px; line-height: 1.5;
  }

  .scheme-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }

  .scheme-tag {
    font-size: 10px; padding: 3px 8px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text2);
  }

  .scheme-pros { font-size: 12px; color: var(--text2); line-height: 1.6; }
  .scheme-pros span { color: var(--accent2); margin-right: 4px; }

  /* APPLY TABLE */
  .apply-table {
    width: 100%; border-collapse: collapse;
    font-size: 13px; margin-top: 10px;
  }

  .apply-table th {
    background: var(--surface2);
    padding: 10px 14px; text-align: left;
    font-weight: 600; font-size: 11px;
    text-transform: uppercase; color: var(--text2);
    letter-spacing: 0.06em;
    border-bottom: 1px solid var(--border);
  }

  .apply-table td {
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text); vertical-align: top;
  }

  .apply-table tr:last-child td { border-bottom: none; }
  .apply-table tr:hover td { background: rgba(255,255,255,0.02); }

  .step-num {
    width: 26px; height: 26px; border-radius: 50%;
    background: var(--accent); color: #fff;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; margin-right: 10px;
    flex-shrink: 0;
  }

  /* CHAT INPUT */
  .chat-input-area {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 14px 16px;
  }

  .chat-input-row { display: flex; gap: 10px; align-items: flex-end; }

  .chat-input {
    flex: 1;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; color: var(--text);
    font-family: var(--font-main); font-size: 13.5px;
    padding: 10px 14px; outline: none;
    resize: none; transition: border-color 0.2s;
    min-height: 44px; max-height: 120px;
  }

  .chat-input:focus { border-color: var(--accent); }
  .chat-input::placeholder { color: var(--text2); }

  .send-btn {
    width: 44px; height: 44px;
    background: var(--accent); border: none; border-radius: 10px;
    color: #fff; font-size: 18px; cursor: pointer;
    transition: all 0.2s; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
  }

  .send-btn:hover { background: #0891b2; }
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

  .quick-questions { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }

  .quick-q {
    font-size: 11px; padding: 5px 10px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 14px; color: var(--text2);
    cursor: pointer; transition: all 0.18s; font-family: var(--font-main);
  }

  .quick-q:hover { border-color: var(--accent); color: var(--accent); }

  /* THINKING */
  .thinking {
    display: flex; align-items: center; gap: 6px;
    font-size: 12px; color: var(--text2);
    padding: 10px 14px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 12px; width: fit-content;
    border-bottom-left-radius: 4px;
  }

  .dots span {
    animation: blink 1.4s infinite both;
    font-size: 18px; line-height: 1;
  }
  .dots span:nth-child(2) { animation-delay: 0.2s; }
  .dots span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes blink { 0%,80%,100% { opacity:0; } 40% { opacity:1; } }

  /* MARKDOWN */
  code {
    background: var(--surface2); padding: 2px 5px;
    border-radius: 4px; font-family: monospace;
    font-size: 12px; color: var(--accent2);
    border: 1px solid var(--border);
  }

  pre {
    background: var(--surface2); padding: 10px;
    border-radius: 8px; overflow-x: auto;
    border: 1px solid var(--border); margin: 8px 0;
  }

  pre code { background: transparent; padding: 0; border: none; color: var(--text); }
  ul, ol { padding-left: 20px; margin: 6px 0; }
  li { margin-bottom: 4px; }

  strong { color: var(--text); }

  /* MODAL */
  .modal-overlay {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(7,11,20,0.75);
    backdrop-filter: blur(8px);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000; opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease;
  }

  .modal-overlay.active { opacity: 1; pointer-events: auto; }

  .modal-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--card-radius); padding: 24px;
    width: 100%; max-width: 480px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    transform: translateY(20px); transition: transform 0.3s ease;
  }

  .modal-overlay.active .modal-card { transform: translateY(0); }

  .modal-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 20px; border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
  }

  .modal-title { font-size: 16px; font-weight: 700; }

  .modal-close {
    background: transparent; border: none;
    color: var(--text2); font-size: 20px;
    cursor: pointer; transition: color 0.2s;
  }

  .modal-close:hover { color: var(--text); }
  .modal-body { display: flex; flex-direction: column; gap: 16px; }

  .modal-footer {
    display: flex; justify-content: flex-end; gap: 12px;
    margin-top: 24px; border-top: 1px solid var(--border);
    padding-top: 16px;
  }

  .btn-secondary {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 10px 18px; border-radius: 8px;
    cursor: pointer; font-weight: 600; font-size: 13px;
    transition: background-color 0.2s; font-family: var(--font-main);
  }

  .btn-secondary:hover { background: var(--surface); }

  .btn-primary {
    background: var(--accent); border: none;
    color: #fff; padding: 10px 18px; border-radius: 8px;
    cursor: pointer; font-weight: 600; font-size: 13px;
    transition: background-color 0.2s; font-family: var(--font-main);
  }

  .btn-primary:hover { background: #0891b2; }

  .modal-input {
    width: 100%; padding: 9px 12px;
    border-radius: 8px; background: var(--surface2);
    border: 1px solid var(--border); color: var(--text);
    font-family: var(--font-main); font-size: 13px; outline: none;
  }

  .modal-input:focus { border-color: var(--accent); }

  .hidden { display: none !important; }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  /* EMPTY STATE */
  .empty-state {
    text-align: center; padding: 60px 20px;
    color: var(--text2); font-size: 14px;
  }
  .empty-state .icon { font-size: 48px; margin-bottom: 16px; }

  /* PORTAL LINK */
  .portal-link {
    display: inline-flex; align-items: center; gap: 6px;
    color: var(--accent); font-size: 12px; font-weight: 600;
    text-decoration: none; margin-top: 8px;
    border: 1px solid rgba(6,182,212,0.3);
    padding: 4px 10px; border-radius: 8px;
    transition: all 0.2s;
  }
  .portal-link:hover { background: rgba(6,182,212,0.1); }
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="logo">
    <div class="logo-icon">🏛️</div>
    <div class="logo-text">
      <h1 id="header-title">SAHAY - Scheme Finder</h1>
      <p id="header-sub">AI-Powered · 4 Languages · Hyderabad Ready</p>
    </div>
  </div>
  <div class="header-actions">
    <div class="lang-switcher">
      <button class="lang-btn active" onclick="setLang('en')" id="btn-en">EN</button>
      <button class="lang-btn" onclick="setLang('hi')" id="btn-hi">हिं</button>
      <button class="lang-btn" onclick="setLang('te')" id="btn-te">తె</button>
      <button class="lang-btn" onclick="setLang('ta')" id="btn-ta">தமி</button>
    </div>
    <button class="icon-btn" onclick="openSettings()">
      <span>⚙️</span> <span data-i18n="settings_btn">Settings</span>
    </button>
  </div>
</div>

<div class="container">
  <!-- SIDEBAR -->
  <aside>
    <div class="section-card">
      <div class="section-title">🔍 <span data-i18n="filters_title">Filters</span></div>

      <div class="form-group">
        <label data-i18n="category_label">Scheme Category</label>
        <div class="chips" id="category-chips">
          <div class="chip selected" data-val="all" onclick="toggleCategory(this)">✅ All</div>
          <div class="chip" data-val="health" onclick="toggleCategory(this)">🏥 Health</div>
          <div class="chip" data-val="education" onclick="toggleCategory(this)">📚 Education</div>
          <div class="chip" data-val="agriculture" onclick="toggleCategory(this)">🌾 Agriculture</div>
          <div class="chip" data-val="housing" onclick="toggleCategory(this)">🏠 Housing</div>
          <div class="chip" data-val="women" onclick="toggleCategory(this)">👩 Women</div>
          <div class="chip" data-val="employment" onclick="toggleCategory(this)">💼 Employment</div>
          <div class="chip" data-val="pension" onclick="toggleCategory(this)">🪙 Pension</div>
        </div>
      </div>

      <div class="form-group">
        <label data-i18n="state_label">Your State</label>
        <select id="user-state">
          <option value="all">All India (Central Schemes)</option>
          <option value="telangana">Telangana / తెలంగాణ</option>
          <option value="andhra">Andhra Pradesh / ఆంధ్రప్రదేశ్</option>
          <option value="tamilnadu">Tamil Nadu / தமிழ்நாடு</option>
          <option value="karnataka">Karnataka / ಕರ್ನಾಟಕ</option>
          <option value="maharashtra">Maharashtra / महाराष्ट्र</option>
          <option value="delhi">Delhi / दिल्ली</option>
        </select>
      </div>

      <div class="form-group">
        <label data-i18n="income_label">Annual Family Income</label>
        <div class="budget-display" id="income-display">₹2.5 Lakh</div>
        <input type="range" min="1" max="20" value="2" id="income-slider" oninput="updateIncome(this.value)" step="1">
        <div class="slider-labels">
          <span>₹0</span>
          <span>₹10L</span>
          <span>₹20L+</span>
        </div>
      </div>

      <div class="form-group">
        <label data-i18n="age_label">Age Group</label>
        <select id="user-age">
          <option value="any">Any</option>
          <option value="youth">Youth (18–35)</option>
          <option value="adult">Adult (35–60)</option>
          <option value="senior">Senior (60+)</option>
        </select>
      </div>

      <button class="cta-btn" id="find-schemes-btn" onclick="findSchemes()">
        <span>🔍</span>
        <span data-i18n="find_schemes_btn">Find My Schemes</span>
      </button>
    </div>

    <!-- QUICK INFO -->
    <div class="section-card">
      <div class="section-title">💡 <span data-i18n="tip_title">Quick Tip</span></div>
      <p style="font-size:12.5px;color:var(--text2);line-height:1.7;" data-i18n="tip_text">
        Ask the AI in your language! Try: "मुझे कौन सी योजनाएं मिलेंगी?" or "నాకు ఏ పథకాలు వర్తిస్తాయి?"
      </p>
    </div>
  </aside>

  <!-- MAIN -->
  <main>
    <!-- HERO -->
    <div class="hero">
      <h2 data-i18n="hero_title">Find Government Schemes You Actually Qualify For</h2>
      <p data-i18n="hero_desc">Tell SAHAY your profile and ask questions in Telugu, Hindi, Tamil, or English. We search 1000+ Central and State schemes to find benefits you may be missing.</p>
      <div class="stats-row">
        <div class="stat">
          <span class="stat-val">1000+</span>
          <span class="stat-label" data-i18n="stat_schemes">Schemes</span>
        </div>
        <div class="stat">
          <span class="stat-val">4</span>
          <span class="stat-label" data-i18n="stat_langs">Languages</span>
        </div>
        <div class="stat">
          <span class="stat-val">28+</span>
          <span class="stat-label" data-i18n="stat_states">States Covered</span>
        </div>
        <div class="stat">
          <span class="stat-val">100%</span>
          <span class="stat-label" data-i18n="stat_free">Free</span>
        </div>
      </div>
    </div>

    <!-- TABS -->
    <div class="tabs">
      <button class="tab active" onclick="switchTab('chat', this)">
        <span data-i18n="tab_chat">💬 AI Chat</span>
      </button>
      <button class="tab" onclick="switchTab('schemes', this)" style="position:relative;">
        <span data-i18n="tab_schemes">📋 Schemes</span>
        <span id="schemes-dot" class="hidden" style="position:absolute;top:6px;right:6px;width:6px;height:6px;background:var(--accent2);border-radius:50%;"></span>
      </button>
      <button class="tab" onclick="switchTab('apply', this)" style="position:relative;">
        <span data-i18n="tab_apply">📝 How to Apply</span>
        <span id="apply-dot" class="hidden" style="position:absolute;top:6px;right:6px;width:6px;height:6px;background:var(--accent2);border-radius:50%;"></span>
      </button>
    </div>

    <!-- CHAT TAB -->
    <div id="tab-chat">
      <div class="chat-area">
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="ai-status-dot"></div>
            <span style="font-size:13px;font-weight:600;" data-i18n="ai_name">SAHAY AI Assistant</span>
          </div>
          <span id="model-badge" style="font-size:11px;color:var(--accent2);">⚡ Gemini Mode</span>
        </div>
        <div class="chat-messages" id="chat-messages">
          <div class="msg ai">
            <div class="msg-avatar">🏛️</div>
            <div class="msg-bubble" id="welcome-msg">
              Namaste! 🙏 I'm <strong>SAHAY</strong> — your AI guide to Indian government schemes.<br><br>
              I speak <strong>English, हिंदी, తెలుగు, and தமிழ்</strong>. Tell me your income, state, age, and needs — I'll find schemes you qualify for!<br>
              <em>Try asking: "What health schemes are available in Telangana?" or "నాకు వ్యవసాయ పథకాలు ఏమైనా ఉన్నాయా?"</em>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <div class="chat-input-row">
          <textarea class="chat-input" id="chat-input" placeholder="Ask about any scheme... / कोई भी योजना पूछें... / ఏదైనా పథకం అడగండి..." rows="1" onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
          <button class="send-btn" id="send-btn" onclick="sendMessage()">➤</button>
        </div>
        <div class="quick-questions" id="quick-questions">
          <span class="quick-q" onclick="askQuick(this)">Best health schemes in Telangana?</span>
          <span class="quick-q" onclick="askQuick(this)">Farmer schemes for 2 acres land?</span>
          <span class="quick-q" onclick="askQuick(this)">Education scholarships for SC/ST?</span>
          <span class="quick-q" onclick="askQuick(this)">Housing schemes for BPL families?</span>
          <span class="quick-q" onclick="askQuick(this)">మహిళలకు పథకాలు ఏమిటి?</span>
        </div>
      </div>
    </div>

    <!-- SCHEMES TAB -->
    <div id="tab-schemes" class="hidden">
      <div id="schemes-placeholder" class="empty-state">
        <div class="icon">🔍</div>
        <span data-i18n="no_schemes_yet">Set your filters and click "Find My Schemes" to discover benefits.</span>
      </div>
      <div class="scheme-cards" id="scheme-cards"></div>
    </div>

    <!-- APPLY TAB -->
    <div id="tab-apply" class="hidden">
      <div id="apply-placeholder" class="empty-state">
        <div class="icon">📝</div>
        <span data-i18n="no_apply_yet">Click on a scheme card to see step-by-step application guide.</span>
      </div>
      <div id="apply-content"></div>
    </div>

  </main>
</div>

<!-- SETTINGS MODAL -->
<div class="modal-overlay" id="settings-modal">
  <div class="modal-card">
    <div class="modal-header">
      <h3 class="modal-title" data-i18n="settings_title">⚙️ AI Settings</h3>
      <button class="modal-close" onclick="closeSettings()">&times;</button>
    </div>
    <div class="modal-body">
      <div class="form-group">
        <label data-i18n="provider_label">API Provider</label>
        <select id="setting-provider" class="modal-input" onchange="onProviderChange()">
          <option value="gemini">Google Gemini</option>
          <option value="custom">Custom (OpenAI Compatible)</option>
        </select>
      </div>
      <div class="form-group">
        <label data-i18n="base_url_label">API Base URL</label>
        <input type="text" id="setting-base-url" class="modal-input" placeholder="https://generativelanguage.googleapis.com/v1beta/openai">
      </div>
      <div class="form-group">
        <label data-i18n="api_key_label">API Key</label>
        <input type="password" id="setting-api-key" class="modal-input" placeholder="Enter API Key">
      </div>
      <div class="form-group">
        <label data-i18n="model_label">Model Name</label>
        <input type="text" id="setting-model" class="modal-input" placeholder="gemini-2.5-flash-lite">
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn-secondary" onclick="closeSettings()" data-i18n="cancel_btn">Cancel</button>
      <button class="btn-primary" onclick="saveSettings()" data-i18n="save_btn">Save</button>
    </div>
  </div>
</div>

<script>
// ============================================================
// i18n ENGINE
// ============================================================
const TRANSLATIONS = {
  en: {
    'header-title': 'SAHAY - Scheme Finder',
    'header-sub': 'AI-Powered · 4 Languages · India Ready',
    'filters_title': 'Filters',
    'category_label': 'Scheme Category',
    'state_label': 'Your State',
    'income_label': 'Annual Family Income',
    'age_label': 'Age Group',
    'find_schemes_btn': 'Find My Schemes',
    'tip_title': 'Quick Tip',
    'tip_text': 'Ask the AI in your language! Try: "What schemes help farmers?" or "నాకు ఏ పథకాలు వర్తిస్తాయి?"',
    'hero_title': 'Find Government Schemes You Actually Qualify For',
    'hero_desc': 'Tell SAHAY your profile and ask questions in Telugu, Hindi, Tamil, or English. We search 1000+ Central and State schemes to find benefits you may be missing.',
    'stat_schemes': 'Schemes',
    'stat_langs': 'Languages',
    'stat_states': 'States Covered',
    'stat_free': 'Free',
    'tab_chat': '💬 AI Chat',
    'tab_schemes': '📋 Schemes',
    'tab_apply': '📝 How to Apply',
    'ai_name': 'SAHAY AI Assistant',
    'no_schemes_yet': 'Set your filters and click "Find My Schemes" to discover benefits.',
    'no_apply_yet': 'Click on a scheme card to see step-by-step application guide.',
    'settings_btn': 'Settings',
    'settings_title': '⚙️ AI Settings',
    'provider_label': 'API Provider',
    'base_url_label': 'API Base URL',
    'api_key_label': 'API Key',
    'model_label': 'Model Name',
    'cancel_btn': 'Cancel',
    'save_btn': 'Save',
    'welcome': 'Namaste! 🙏 I\'m <strong>SAHAY</strong> — your AI guide to Indian government schemes.<br><br>I speak <strong>English, हिंदी, తెలుగు, and தமிழ்</strong>. Tell me your income, state, age, and needs — I\'ll find schemes you qualify for!<br><em>Try: "What health schemes are in Telangana?" or "నాకు వ్యవసాయ పథకాలు ఏమైనా ఉన్నాయా?"</em>',
    'quick_qs': ['Best health schemes in Telangana?', 'Farmer schemes for 2 acres land?', 'Education scholarships for SC/ST?', 'Housing schemes for BPL families?', 'మహిళలకు పథకాలు ఏమిటి?'],
    'chat_placeholder': 'Ask about any scheme... / ఏదైనా పథకం అడగండి...',
    'match': 'Match',
  },
  hi: {
    'header-title': 'सहाय - योजना खोज',
    'header-sub': 'AI-संचालित · 4 भाषाएं · भारत तैयार',
    'filters_title': 'फ़िल्टर',
    'category_label': 'योजना श्रेणी',
    'state_label': 'आपका राज्य',
    'income_label': 'वार्षिक पारिवारिक आय',
    'age_label': 'आयु वर्ग',
    'find_schemes_btn': 'मेरी योजनाएं खोजें',
    'tip_title': 'त्वरित सुझाव',
    'tip_text': 'AI से हिंदी में पूछें! जैसे: "मुझे कौन सी योजनाएं मिलेंगी?" या "किसानों के लिए क्या है?"',
    'hero_title': 'वो सरकारी योजनाएं खोजें जिनके आप हकदार हैं',
    'hero_desc': 'SAHAY को अपनी जानकारी दें और हिंदी, तेलुगु, तमिल, या अंग्रेजी में सवाल पूछें। हम 1000+ केंद्रीय और राज्य योजनाएं खोजते हैं।',
    'stat_schemes': 'योजनाएं',
    'stat_langs': 'भाषाएं',
    'stat_states': 'राज्य शामिल',
    'stat_free': 'मुफ़्त',
    'tab_chat': '💬 AI चैट',
    'tab_schemes': '📋 योजनाएं',
    'tab_apply': '📝 कैसे आवेदन करें',
    'ai_name': 'SAHAY AI सहायक',
    'no_schemes_yet': 'फ़िल्टर सेट करें और "मेरी योजनाएं खोजें" पर क्लिक करें।',
    'no_apply_yet': 'चरण-दर-चरण आवेदन गाइड देखने के लिए किसी योजना कार्ड पर क्लिक करें।',
    'settings_btn': 'सेटिंग्स',
    'settings_title': '⚙️ AI सेटिंग्स',
    'provider_label': 'API प्रदाता',
    'base_url_label': 'API बेस URL',
    'api_key_label': 'API कुंजी',
    'model_label': 'मॉडल नाम',
    'cancel_btn': 'रद्द करें',
    'save_btn': 'सहेजें',
    'welcome': 'नमस्ते! 🙏 मैं <strong>SAHAY</strong> हूं — भारतीय सरकारी योजनाओं का आपका AI गाइड।<br><br>मैं <strong>हिंदी, English, తెలుగు, और தமிழ்</strong> में बात कर सकता हूं। अपनी आय, राज्य, उम्र बताएं — मैं आपके लिए योजनाएं खोजूंगा!<br><em>पूछें: "किसानों के लिए कौन सी योजनाएं हैं?" या "आयुष्मान भारत के बारे में बताओ?"</em>',
    'quick_qs': ['तेलंगाना में स्वास्थ्य योजनाएं?', 'किसानों के लिए PM-KISAN क्या है?', 'SC/ST के लिए छात्रवृत्ति?', 'BPL परिवारों के लिए आवास?', 'महिलाओं की योजनाएं बताएं'],
    'chat_placeholder': 'कोई भी योजना पूछें... / Ask about any scheme...',
    'match': 'मिलान',
  },
  te: {
    'header-title': 'సహాయ్ - పథకాల వెతుకులాట',
    'header-sub': 'AI ఆధారిత · 4 భాషలు · భారత్ కోసం',
    'filters_title': 'వడపోతలు',
    'category_label': 'పథక వర్గం',
    'state_label': 'మీ రాష్ట్రం',
    'income_label': 'వార్షిక కుటుంబ ఆదాయం',
    'age_label': 'వయస్సు వర్గం',
    'find_schemes_btn': 'నా పథకాలు కనుగొనండి',
    'tip_title': 'త్వరిత చిట్కా',
    'tip_text': 'AI ని తెలుగులో అడగండి! ఉదా: "నాకు ఏ పథకాలు వర్తిస్తాయి?" లేదా "రైతులకు పథకాలు ఏమిటి?"',
    'hero_title': 'మీకు అర్హత ఉన్న ప్రభుత్వ పథకాలు కనుగొనండి',
    'hero_desc': 'SAHAY కి మీ వివరాలు చెప్పండి, తెలుగు, హిందీ, తమిళం లేదా ఇంగ్లీష్‌లో అడగండి. 1000+ కేంద్ర మరియు రాష్ట్ర పథకాలు వెతుకుతాం.',
    'stat_schemes': 'పథకాలు',
    'stat_langs': 'భాషలు',
    'stat_states': 'రాష్ట్రాలు',
    'stat_free': 'ఉచిత',
    'tab_chat': '💬 AI చాట్',
    'tab_schemes': '📋 పథకాలు',
    'tab_apply': '📝 దరఖాస్తు ఎలా',
    'ai_name': 'SAHAY AI సహాయకుడు',
    'no_schemes_yet': 'వడపోతలు సెట్ చేసి "నా పథకాలు కనుగొనండి" క్లిక్ చేయండి.',
    'no_apply_yet': 'దశల వారీ దరఖాస్తు గైడ్ చూడటానికి పథక కార్డ్ పై క్లిక్ చేయండి.',
    'settings_btn': 'సెట్టింగులు',
    'settings_title': '⚙️ AI సెట్టింగులు',
    'provider_label': 'API సేవాదాత',
    'base_url_label': 'API బేస్ URL',
    'api_key_label': 'API కీ',
    'model_label': 'మోడల్ పేరు',
    'cancel_btn': 'రద్దు చేయి',
    'save_btn': 'సేవ్ చేయి',
    'welcome': 'నమస్కారం! 🙏 నేను <strong>SAHAY</strong> — భారత ప్రభుత్వ పథకాలకు మీ AI గైడ్.<br><br>నేను <strong>తెలుగు, English, हिंदी, மற்றும் தமிழ்</strong> లో మాట్లాడగలను. మీ ఆదాయం, రాష్ట్రం, వయస్సు చెప్పండి — మీకు అర్హమైన పథకాలు కనుగొంటాను!<br><em>అడగండి: "తెలంగాణలో ఆరోగ్య పథకాలు ఏమిటి?" లేదా "PM-KISAN గురించి చెప్పండి"</em>',
    'quick_qs': ['తెలంగాణలో ఆరోగ్య పథకాలు?', 'రైతులకు PM-KISAN అంటే ఏమిటి?', 'SC/ST విద్యార్థులకు స్కాలర్‌షిప్?', 'BPL కుటుంబాలకు గృహ పథకాలు?', 'మహిళలకు పథకాలు ఏమిటి?'],
    'chat_placeholder': 'ఏదైనా పథకం అడగండి... / Ask about any scheme...',
    'match': 'సరిపోలిక',
  },
  ta: {
    'header-title': 'சகாய் - திட்ட தேடல்',
    'header-sub': 'AI இயங்கும் · 4 மொழிகள் · இந்தியா தயார்',
    'filters_title': 'வடிகட்டிகள்',
    'category_label': 'திட்ட வகை',
    'state_label': 'உங்கள் மாநிலம்',
    'income_label': 'ஆண்டு குடும்ப வருமானம்',
    'age_label': 'வயதுப் பிரிவு',
    'find_schemes_btn': 'என் திட்டங்களை கண்டறி',
    'tip_title': 'விரைவு குறிப்பு',
    'tip_text': 'AI ஐ தமிழில் கேளுங்கள்! எ.கா: "எனக்கு என்ன திட்டங்கள் கிடைக்கும்?" அல்லது "விவசாயிகளுக்கான திட்டங்கள்?"',
    'hero_title': 'உங்களுக்கு தகுதியான அரசு திட்டங்களை கண்டறியுங்கள்',
    'hero_desc': 'SAHAY க்கு உங்கள் விவரங்களை சொல்லுங்கள், தமிழ், தெலுங்கு, இந்தி அல்லது ஆங்கிலத்தில் கேளுங்கள். 1000+ திட்டங்களை தேடுகிறோம்.',
    'stat_schemes': 'திட்டங்கள்',
    'stat_langs': 'மொழிகள்',
    'stat_states': 'மாநிலங்கள்',
    'stat_free': 'இலவசம்',
    'tab_chat': '💬 AI அரட்டை',
    'tab_schemes': '📋 திட்டங்கள்',
    'tab_apply': '📝 விண்ணப்பிக்க',
    'ai_name': 'SAHAY AI உதவியாளர்',
    'no_schemes_yet': 'வடிகட்டிகளை அமைத்து "என் திட்டங்களை கண்டறி" என்பதை கிளிக் செய்யுங்கள்.',
    'no_apply_yet': 'படிப்படியான விண்ணப்ப வழிகாட்டலுக்கு திட்ட அட்டையில் கிளிக் செய்யுங்கள்.',
    'settings_btn': 'அமைப்புகள்',
    'settings_title': '⚙️ AI அமைப்புகள்',
    'provider_label': 'API வழங்குனர்',
    'base_url_label': 'API அடிப்படை URL',
    'api_key_label': 'API திறவுகோல்',
    'model_label': 'மாதிரி பெயர்',
    'cancel_btn': 'ரத்து செய்',
    'save_btn': 'சேமி',
    'welcome': 'வணக்கம்! 🙏 நான் <strong>SAHAY</strong> — இந்திய அரசு திட்டங்களுக்கான உங்கள் AI வழிகாட்டி.<br><br>நான் <strong>தமிழ், English, తెలుగు, और हिंदी</strong> பேசுகிறேன். உங்கள் வருமானம், மாநிலம், வயது சொல்லுங்கள் — தகுதியான திட்டங்களை கண்டறிகிறேன்!<br><em>கேளுங்கள்: "தமிழ்நாட்டில் உடல்நல திட்டங்கள்?" அல்லது "விவசாயிகளுக்கான திட்டங்கள் என்ன?"</em>',
    'quick_qs': ['தமிழ்நாட்டில் சுகாதார திட்டங்கள்?', 'விவசாயிகளுக்கு PM-KISAN என்ன?', 'SC/ST மாணவர்களுக்கு உதவித்தொகை?', 'BPL குடும்பங்களுக்கு வீட்டு திட்டங்கள்?', 'மகளிருக்கான திட்டங்கள் என்ன?'],
    'chat_placeholder': 'எந்த திட்டத்தையும் கேளுங்கள்... / Ask about any scheme...',
    'match': 'பொருத்தம்',
  }
};

// ============================================================
// SCHEME DATABASE
// ============================================================
const SCHEME_DB = [
  {
    id: 'pm-kisan',
    name: 'PM-KISAN',
    fullName: 'Pradhan Mantri Kisan Samman Nidhi',
    category: 'agriculture',
    ministry: 'Ministry of Agriculture',
    benefit: '₹6,000/year',
    state: 'all',
    eligibility: 'Small & marginal farmers with landholding up to 2 hectares',
    match: 95,
    pros: ['Direct bank transfer ₹2000 × 3 installments', 'No middlemen', 'Covers 11 crore+ farmers'],
    portal: 'https://pmkisan.gov.in',
    applySteps: [
      { step: 'Visit pmkisan.gov.in or nearest CSC center', detail: 'Carry Aadhaar, land documents, bank passbook' },
      { step: 'Fill farmer registration form', detail: 'Enter Aadhaar, bank account, mobile number' },
      { step: 'Land verification by local patwari', detail: 'Usually takes 7-15 working days' },
      { step: 'Get approved & receive first installment', detail: 'Amount directly credited to bank account' }
    ]
  },
  {
    id: 'ayushman',
    name: 'Ayushman Bharat PM-JAY',
    fullName: 'Pradhan Mantri Jan Arogya Yojana',
    category: 'health',
    ministry: 'Ministry of Health & Family Welfare',
    benefit: '₹5 Lakh/year health cover',
    state: 'all',
    eligibility: 'SECC-listed families, BPL households, construction workers, rag pickers',
    match: 92,
    pros: ['Cashless treatment at 25,000+ hospitals', 'No premium for beneficiary', 'Covers 1,400+ medical procedures'],
    portal: 'https://pmjay.gov.in',
    applySteps: [
      { step: 'Check eligibility at pmjay.gov.in', detail: 'Enter Aadhaar/Ration card number to verify' },
      { step: 'Visit nearest Ayushman Mitra center', detail: 'At government hospitals or CSC centers' },
      { step: 'Get Ayushman card (Golden Card)', detail: 'Biometric verification with Aadhaar' },
      { step: 'Use card at any empanelled hospital', detail: 'Show card at hospital counter for cashless treatment' }
    ]
  },
  {
    id: 'pmay-gramin',
    name: 'PMAY-Gramin',
    fullName: 'Pradhan Mantri Awaas Yojana - Gramin',
    category: 'housing',
    ministry: 'Ministry of Rural Development',
    benefit: '₹1.2–2 Lakh subsidy',
    state: 'all',
    eligibility: 'Homeless/kutcha house families in SECC list, BPL rural households',
    match: 88,
    pros: ['Full house construction assistance', 'MGNREGS wage for 90 days', 'Sanitation support included'],
    portal: 'https://pmayg.nic.in',
    applySteps: [
      { step: 'Check SECC/Awaas+ list in Gram Sabha', detail: 'List published at Panchayat office' },
      { step: 'Submit application to Gram Panchayat', detail: 'Provide Aadhaar, bank account, land docs' },
      { step: 'Geo-tagged progress photos required', detail: 'Uploaded by local Gram Rozgar Sevak' },
      { step: 'Funds released in 3 installments', detail: 'Based on construction progress verification' }
    ]
  },
  {
    id: 'sukanya',
    name: 'Sukanya Samriddhi Yojana',
    fullName: 'Sukanya Samriddhi Account Scheme',
    category: 'women',
    ministry: 'Ministry of Finance',
    benefit: '8.2% interest rate (tax-free)',
    state: 'all',
    eligibility: 'Girl child below 10 years, by parents/guardians',
    match: 87,
    pros: ['Highest guaranteed return among small savings', 'Tax exemption under 80C', 'Matures when girl turns 21'],
    portal: 'https://www.indiapost.gov.in',
    applySteps: [
      { step: 'Visit Post Office or any nationalized bank', detail: 'Carry girl\'s birth certificate, parent Aadhaar' },
      { step: 'Fill SSY account opening form', detail: 'Minimum deposit ₹250, maximum ₹1.5 lakh/year' },
      { step: 'Get account passbook', detail: 'Deposits can be made anytime up to 15 years' },
      { step: 'Partial withdrawal at age 18 (50%)', detail: 'Full maturity at 21 years of girl' }
    ]
  },
  {
    id: 'mudra',
    name: 'PM MUDRA Yojana',
    fullName: 'Pradhan Mantri Micro Units Development & Refinance Agency',
    category: 'employment',
    ministry: 'Ministry of Finance',
    benefit: 'Loans up to ₹10 Lakh (no collateral)',
    state: 'all',
    eligibility: 'Non-farm micro/small enterprises, self-employed persons, small manufacturers',
    match: 83,
    pros: ['Shishu (₹50K), Kishore (₹5L), Tarun (₹10L)', 'No collateral required', 'Low interest rates'],
    portal: 'https://www.mudra.org.in',
    applySteps: [
      { step: 'Prepare business plan / existing business details', detail: 'Include income proof, bank statements 6 months' },
      { step: 'Visit bank/NBFC/MFI of your choice', detail: 'Any scheduled commercial bank accepts MUDRA applications' },
      { step: 'Submit application with documents', detail: 'Aadhaar, PAN, address proof, business proof' },
      { step: 'Loan disbursed to account in 7–15 days', detail: 'MUDRA card issued for working capital needs' }
    ]
  },
  {
    id: 'aarogyasri',
    name: 'Aarogyasri Health Care Trust',
    fullName: 'Chief Minister\'s Comprehensive Health Care for Poor (TS)',
    category: 'health',
    ministry: 'Government of Telangana',
    benefit: '₹5 Lakh/year + ₹2 Lakh accident cover',
    state: 'telangana',
    eligibility: 'White Ration Card holders in Telangana',
    match: 96,
    pros: ['2200+ covered surgical procedures', 'Cashless at 250+ network hospitals', 'Covers pre & post hospitalization'],
    portal: 'https://www.aarogyasri.telangana.gov.in',
    applySteps: [
      { step: 'Have a valid White Ration Card (Telangana)', detail: 'Check eligibility at Aarogyasri website' },
      { step: 'Go to empanelled hospital for treatment', detail: 'Show ration card + Aadhaar at Aarogyasri desk' },
      { step: 'Pre-authorization done at hospital', detail: 'Takes 30–60 minutes for approval' },
      { step: 'Treatment provided cashless', detail: 'Discharge with zero payment for covered procedures' }
    ]
  },
  {
    id: 'rythu-bandhu',
    name: 'Rythu Bandhu',
    fullName: 'Telangana Rythu Bandhu Scheme',
    category: 'agriculture',
    ministry: 'Government of Telangana',
    benefit: '₹10,000/acre/year (2 seasons)',
    state: 'telangana',
    eligibility: 'All landholding farmers in Telangana with valid Pattadar Passbook',
    match: 97,
    pros: ['₹5000 per acre per season', 'Direct to farmer bank account', 'No loan required'],
    portal: 'https://rythubandhu.telangana.gov.in',
    applySteps: [
      { step: 'Verify your Pattadar Passbook is updated', detail: 'Carry it to nearest Mee Seva center if issues' },
      { step: 'Check beneficiary list at village level', detail: 'List published before each season (Kharif/Rabi)' },
      { step: 'Ensure bank account linked to Aadhaar', detail: 'Visit bank for Aadhaar seeding if not done' },
      { step: 'Amount credited automatically each season', detail: 'No application needed if already registered' }
    ]
  },
  {
    id: 'mgnregs',
    name: 'MGNREGS',
    fullName: 'Mahatma Gandhi National Rural Employment Guarantee Scheme',
    category: 'employment',
    ministry: 'Ministry of Rural Development',
    benefit: '100 days of guaranteed employment/year',
    state: 'all',
    eligibility: 'Any adult member of rural household willing to do unskilled manual work',
    match: 85,
    pros: ['₹220–300/day wage (state-wise)', 'Work within 5km of home', 'Unemployment allowance if work not given in 15 days'],
    portal: 'https://nrega.nic.in',
    applySteps: [
      { step: 'Apply for Job Card at Gram Panchayat', detail: 'Provide Aadhaar, photo, bank account details' },
      { step: 'Receive MGNREGA Job Card within 15 days', detail: 'Free of cost, names of all adult family members' },
      { step: 'Submit work demand application (Form 6)', detail: 'At Gram Panchayat or online at MGNREGS portal' },
      { step: 'Work allotted within 15 days', detail: 'Wages paid within 15 days of work completion' }
    ]
  },
  {
    id: 'ujjwala',
    name: 'PM Ujjwala Yojana',
    fullName: 'Pradhan Mantri Ujjwala Yojana 2.0',
    category: 'women',
    ministry: 'Ministry of Petroleum and Natural Gas',
    benefit: 'Free LPG connection + first cylinder',
    state: 'all',
    eligibility: 'Women from BPL/SC/ST/PMAY/forest dwellers/migrants households, 18+ years',
    match: 89,
    pros: ['Free cylinder + regulator + stove', 'No deposit required', 'EMI option for stove purchase'],
    portal: 'https://www.pmuy.gov.in',
    applySteps: [
      { step: 'Visit nearest LPG distributor (IOC/HP/BP)', detail: 'Carry Aadhaar, BPL/ration card, bank passbook' },
      { step: 'Submit KYC form at distributor', detail: 'Self-declaration of BPL status accepted' },
      { step: 'Connection approved in 3–5 working days', detail: 'Cylinder delivered to address provided' },
      { step: 'Avail subsidy on subsequent cylinders', detail: 'Directly credited to bank account per cylinder' }
    ]
  },
  {
    id: 'atal-pension',
    name: 'Atal Pension Yojana',
    fullName: 'Atal Pension Yojana (APY)',
    category: 'pension',
    ministry: 'Ministry of Finance / PFRDA',
    benefit: '₹1,000–₹5,000 guaranteed monthly pension',
    state: 'all',
    eligibility: 'Indian citizens aged 18–40, not income tax payer, with savings bank account',
    match: 78,
    pros: ['Government co-contributes 50% (for eligible)', 'Spouse gets pension after death', 'Nominee gets corpus'],
    portal: 'https://www.npscra.nsdl.co.in',
    applySteps: [
      { step: 'Visit your savings bank account branch', detail: 'Any bank or post office offers APY enrollment' },
      { step: 'Fill APY enrollment form', detail: 'Choose pension amount ₹1K–5K, nominee details' },
      { step: 'Auto-debit set up from bank account', detail: 'Monthly contribution based on age & pension chosen' },
      { step: 'Receive pension from age 60', detail: 'Or exit early after 10 years minimum contribution' }
    ]
  },
  {
    id: 'nmms',
    name: 'NMMS Scholarship',
    fullName: 'National Means-cum-Merit Scholarship Scheme',
    category: 'education',
    ministry: 'Ministry of Education',
    benefit: '₹12,000/year (₹1,000/month) for 4 years',
    state: 'all',
    eligibility: 'Class 8 students from government schools, family income < ₹3.5L/year, >55% in Class 7',
    match: 80,
    pros: ['Direct scholarship for Class 9–12', 'No repayment required', 'Encourages merit in low-income students'],
    portal: 'https://scholarships.gov.in',
    applySteps: [
      { step: 'Clear State-level NMMS exam (Nov)', detail: 'School nominates eligible Class 8 students' },
      { step: 'Get MAT + SAT scores (qualifying cutoff)', detail: 'Minimum 40% (32% for SC/ST)' },
      { step: 'Apply on National Scholarship Portal', detail: 'Upload income certificate, school certificate, Aadhaar' },
      { step: 'Scholarship renewed yearly with 55% marks', detail: 'Direct credit to student bank account' }
    ]
  },
  {
    id: 'post-matric-scst',
    name: 'Post-Matric Scholarship SC/ST',
    fullName: 'Post-Matric Scholarship for SC and ST Students',
    category: 'education',
    ministry: 'Ministry of Social Justice & Empowerment',
    benefit: 'Maintenance allowance + tuition fee (varies)',
    state: 'all',
    eligibility: 'SC/ST students studying post-matric (Class 11+), family income < ₹2.5L/year',
    match: 91,
    pros: ['Covers tuition fees completely', 'Maintenance allowance for hostel/day scholars', 'No repayment'],
    portal: 'https://scholarships.gov.in',
    applySteps: [
      { step: 'Register on National Scholarship Portal', detail: 'scholarships.gov.in — use Aadhaar for registration' },
      { step: 'Fill scholarship application form', detail: 'Caste certificate, income certificate, institution details' },
      { step: 'Institute verification of application', detail: 'Nodal officer at your college verifies' },
      { step: 'Amount credited to student account', detail: 'Usually by December–January of academic year' }
    ]
  },
  {
    id: 'cm-relief-ts',
    name: 'CM Relief Fund (TS)',
    fullName: 'Chief Minister\'s Relief Fund - Telangana',
    category: 'health',
    ministry: 'Government of Telangana',
    benefit: 'Up to ₹2 Lakh for medical emergencies',
    state: 'telangana',
    eligibility: 'Telangana residents facing financial hardship due to medical emergencies',
    match: 82,
    pros: ['Covers rare diseases not in Aarogyasri', 'Available for Telangana residents only', 'Direct assistance from government'],
    portal: 'https://cmrelief.telangana.gov.in',
    applySteps: [
      { step: 'Apply online at cmrelief.telangana.gov.in', detail: 'Or submit at District Collectorate office' },
      { step: 'Attach hospital estimates / bills', detail: 'Medical reports and prescription required' },
      { step: 'Application reviewed by district committee', detail: 'Typically 15–30 days process' },
      { step: 'Amount sanctioned & released to hospital/patient', detail: 'Based on severity and income assessment' }
    ]
  }
];

// ============================================================
// STATE MANAGEMENT
// ============================================================
let currentLang = 'en';
let conversationHistory = [];
let selectedCategory = 'all';
let incomeInLakhs = 2.5;
let aiSettings = {
  provider: 'gemini',
  baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai',
  apiKey: '',
  model: 'gemini-2.5-flash-lite'
};

// ============================================================
// i18n ENGINE
// ============================================================
function setLang(lang) {
  currentLang = lang;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + lang).classList.add('active');

  const htmlLangMap = { en: 'en', hi: 'hi', te: 'te', ta: 'ta' };
  document.documentElement.lang = htmlLangMap[lang] || 'en';

  const T = TRANSLATIONS[lang];

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (T[key]) el.textContent = T[key];
  });

  // Dynamic elements
  document.getElementById('header-title').textContent = T['header-title'];
  document.getElementById('header-sub').textContent = T['header-sub'];
  document.getElementById('chat-input').placeholder = T['chat_placeholder'];
  document.getElementById('welcome-msg').innerHTML = T['welcome'];

  // Quick questions
  const qqs = document.getElementById('quick-questions');
  qqs.innerHTML = T['quick_qs'].map(q =>
    `<span class="quick-q" onclick="askQuick(this)">${q}</span>`
  ).join('');

  updateIncome(incomeInLakhs);
  updateModelBadge();
}

// ============================================================
// INCOME SLIDER
// ============================================================
function updateIncome(val) {
  incomeInLakhs = parseFloat(val);
  let display = '';
  if (incomeInLakhs >= 100) {
    display = `₹${(incomeInLakhs / 100).toFixed(1)} Crore`;
  } else {
    display = `₹${incomeInLakhs} Lakh`;
  }
  if (currentLang === 'hi') display += ' प्रति वर्ष';
  if (currentLang === 'te') display += ' సంవత్సరానికి';
  if (currentLang === 'ta') display += ' ஆண்டுக்கு';
  document.getElementById('income-display').textContent = display;
}

// ============================================================
// CATEGORY CHIPS
// ============================================================
function toggleCategory(el) {
  document.querySelectorAll('#category-chips .chip').forEach(c => c.classList.remove('selected'));
  el.classList.add('selected');
  selectedCategory = el.dataset.val;
}

// ============================================================
// TABS
// ============================================================
function switchTab(tab, btn) {
  ['chat', 'schemes', 'apply'].forEach(t => {
    document.getElementById('tab-' + t).classList.toggle('hidden', t !== tab);
  });
  document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (tab === 'schemes') document.getElementById('schemes-dot').classList.add('hidden');
  if (tab === 'apply') document.getElementById('apply-dot').classList.add('hidden');
}

// ============================================================
// SCHEME FINDER LOGIC
// ============================================================
function findSchemes() {
  const btn = document.getElementById('find-schemes-btn');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span><span>Searching...</span>';

  setTimeout(() => {
    const state = document.getElementById('user-state').value;
    const age = document.getElementById('user-age').value;

    let filtered = SCHEME_DB.filter(s => {
      if (selectedCategory !== 'all' && s.category !== selectedCategory) return false;
      if (state !== 'all' && s.state !== 'all' && s.state !== state) return false;
      return true;
    });

    // Boost match for income-based filtering
    filtered = filtered.map(s => {
      let boost = 0;
      if (incomeInLakhs < 3 && ['health', 'housing', 'employment'].includes(s.category)) boost += 5;
      if (incomeInLakhs < 5 && s.category === 'agriculture') boost += 3;
      return { ...s, matchScore: (s.match || 80) + boost };
    });

    filtered.sort((a, b) => b.matchScore - a.matchScore);

    displaySchemes(filtered);

    const T = TRANSLATIONS[currentLang];
    btn.disabled = false;
    btn.innerHTML = `<span>🔍</span><span>${T['find_schemes_btn']}</span>`;
  }, 800);
}

function displaySchemes(schemes) {
  const container = document.getElementById('scheme-cards');
  const placeholder = document.getElementById('schemes-placeholder');

  if (schemes.length === 0) {
    placeholder.classList.remove('hidden');
    container.innerHTML = '';
    return;
  }

  placeholder.classList.add('hidden');
  container.innerHTML = '';

  const catColorMap = {
    health: 'cat-health',
    education: 'cat-education',
    agriculture: 'cat-agriculture',
    housing: 'cat-housing',
    women: 'cat-women',
    employment: 'cat-employment',
    pension: 'cat-pension'
  };

  const catEmoji = {
    health: '🏥', education: '📚', agriculture: '🌾',
    housing: '🏠', women: '👩', employment: '💼', pension: '🪙'
  };

  const T = TRANSLATIONS[currentLang];

  schemes.forEach(s => {
    const div = document.createElement('div');
    div.className = 'scheme-card';
    const catClass = catColorMap[s.category] || 'cat-health';
    div.innerHTML = `
      <div class="scheme-card-header">
        <div class="scheme-category-badge ${catClass}">
          ${catEmoji[s.category] || '📋'} ${s.category.toUpperCase()}
        </div>
        <div class="scheme-name">${s.name}</div>
        <div class="scheme-ministry">${s.ministry}</div>
        <div class="match-badge">${s.matchScore || s.match}% ${T['match'] || 'Match'}</div>
      </div>
      <div class="scheme-card-body">
        <div class="scheme-benefit">${s.benefit}</div>
        <div class="scheme-eligibility">👤 ${s.eligibility}</div>
        <div class="scheme-tags">
          <span class="scheme-tag">📍 ${s.state === 'all' ? 'All India' : s.state}</span>
          <span class="scheme-tag">🏛️ Central</span>
        </div>
        <div class="scheme-pros">
          ${s.pros.map(p => `<span>✓</span>${p}<br>`).join('')}
        </div>
        ${s.portal ? `<a class="portal-link" href="${s.portal}" target="_blank">🔗 Official Portal ↗</a>` : ''}
      </div>
    `;
    div.onclick = (e) => {
      if (!e.target.closest('.portal-link')) showApplyGuide(s);
    };
    container.appendChild(div);
  });

  // Show notification dot
  const activeTab = document.querySelector('.tab.active');
  if (!activeTab || !activeTab.textContent.includes('Schemes')) {
    document.getElementById('schemes-dot').classList.remove('hidden');
  }

  // Also switch to schemes tab
  const tabBtn = document.querySelectorAll('.tab')[1];
  switchTab('schemes', tabBtn);
}

function showApplyGuide(scheme) {
  const content = document.getElementById('apply-content');
  const placeholder = document.getElementById('apply-placeholder');
  placeholder.classList.add('hidden');

  content.innerHTML = `
    <div class="section-card" style="margin-bottom:16px;">
      <div style="display:flex;align-items:flex-start;gap:16px;margin-bottom:16px;">
        <div style="font-size:48px;">📋</div>
        <div>
          <h3 style="font-size:18px;font-weight:700;margin-bottom:4px;">${scheme.name}</h3>
          <p style="font-size:13px;color:var(--text2);margin-bottom:8px;">${scheme.fullName}</p>
          <div style="font-size:20px;font-weight:800;color:var(--accent);">${scheme.benefit}</div>
        </div>
      </div>
      <div style="background:var(--surface2);border-radius:10px;padding:14px;margin-bottom:14px;border:1px solid var(--border);">
        <div style="font-size:11px;font-weight:700;color:var(--accent2);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">✅ Eligibility</div>
        <p style="font-size:13px;color:var(--text);">${scheme.eligibility}</p>
      </div>
      <div style="font-size:11px;font-weight:700;color:var(--accent2);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">📝 Step-by-Step Application</div>
      <table class="apply-table">
        <thead>
          <tr><th>Step</th><th>Action</th><th>Details</th></tr>
        </thead>
        <tbody>
          ${scheme.applySteps.map((s, i) => `
            <tr>
              <td><div class="step-num">${i + 1}</div></td>
              <td style="font-weight:600;">${s.step}</td>
              <td style="color:var(--text2);">${s.detail}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      ${scheme.portal ? `
        <div style="margin-top:16px;padding:12px;background:rgba(6,182,212,0.07);border-radius:10px;border:1px solid rgba(6,182,212,0.2);">
          <div style="font-size:12px;color:var(--text2);margin-bottom:6px;">🔗 Official Portal</div>
          <a href="${scheme.portal}" target="_blank" style="color:var(--accent);font-weight:600;text-decoration:none;">${scheme.portal} ↗</a>
        </div>
      ` : ''}
    </div>
  `;

  const applyTabBtn = document.querySelectorAll('.tab')[2];
  switchTab('apply', applyTabBtn);
}

// ============================================================
// CHAT
// ============================================================
function parseMarkdown(text) {
  if (!text) return '';
  let html = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  const lines = html.split('\n');
  let inList = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('* ') || line.startsWith('- ') || line.startsWith('• ')) {
      if (!inList) { lines[i] = '<ul><li>' + line.substring(2) + '</li>'; inList = true; }
      else { lines[i] = '<li>' + line.substring(2) + '</li>'; }
    } else {
      if (inList) { lines[i] = '</ul>' + lines[i]; inList = false; }
    }
  }
  if (inList) lines[lines.length - 1] += '</ul>';
  html = lines.join('\n').replace(/\n/g, '<br>');
  html = html.replace(/<\/li><br>/g, '</li>').replace(/<\/ul><br>/g, '</ul>').replace(/<pre><code><br>/g, '<pre><code>');
  return html;
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function askQuick(el) {
  document.getElementById('chat-input').value = el.textContent;
  sendMessage();
}

function addMessage(role, content) {
  const container = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.innerHTML = `
    <div class="msg-avatar">${role === 'ai' ? '🏛️' : '👤'}</div>
    <div class="msg-bubble">${content}</div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function addThinking() {
  const container = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = 'msg ai';
  div.id = 'thinking-msg';
  div.innerHTML = `
    <div class="msg-avatar">🏛️</div>
    <div class="thinking">
      <div class="dots">
        <span>⚡</span><span>⚡</span><span>⚡</span>
      </div>
      <span>Searching schemes...</span>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function removeThinking() {
  const t = document.getElementById('thinking-msg');
  if (t) t.remove();
}

function buildSystemPrompt() {
  const state = document.getElementById('user-state').value;
  const age = document.getElementById('user-age').value;

  const langInstruction = {
    en: 'Respond ONLY in English.',
    hi: 'केवल हिंदी में जवाब दें। तकनीकी शब्द अंग्रेजी में ठीक हैं।',
    te: 'తెలుగులో మాత్రమే జవాబివ్వండి. సాంకేతిక పదాలు ఆంగ్లంలో పర్వాలేదు.',
    ta: 'தமிழில் மட்டும் பதில் சொல்லுங்கள். தொழில்நுட்ப சொற்கள் ஆங்கிலத்தில் பரவாயில்லை.'
  }[currentLang];

  const schemeNames = SCHEME_DB.map(s => `${s.name} (${s.category}, ${s.benefit})`).join(', ');

  return `You are SAHAY, an expert AI assistant for Indian government welfare schemes. Your mission: help underserved citizens find schemes they qualify for.

LANGUAGE: ${langInstruction}

USER PROFILE:
- Language/State preference: ${currentLang} / ${state}
- Annual income: ₹${incomeInLakhs} Lakh
- Age group: ${age}
- Category interest: ${selectedCategory}

AVAILABLE SCHEMES IN DATABASE (reference these specifically):
${schemeNames}

CAPABILITIES:
- Recommend specific schemes with eligibility criteria and benefit amounts
- Explain how to apply step-by-step in simple language
- Mention official portal URLs when relevant (pmkisan.gov.in, pmjay.gov.in, scholarships.gov.in etc.)
- Be culturally sensitive — use Indian currency format (₹, Lakh, Crore)
- Format benefits clearly with ₹ amounts
- Prioritize schemes matching user's state and income level
- Keep answers focused and practical (not more than 3-4 paragraphs)
- Always mention if a scheme is Central (All India) or State-specific

If user mentions a scheme name, look it up in your training data and provide accurate details.
Always end with an actionable next step the user can take today.`;
}

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = 'auto';

  addMessage('user', text);
  conversationHistory.push({ role: 'user', content: text });

  document.getElementById('send-btn').disabled = true;
  addThinking();

  try {
    const systemPrompt = buildSystemPrompt();
    const settings = aiSettings;

    const useProxy = window.location.protocol.startsWith('http');
    let url, body;

    if (useProxy) {
      let origin = document.referrer
        ? (() => { try { const u = new URL(document.referrer); return u.origin !== 'null' ? u.origin : window.location.origin; } catch(e) { return window.location.origin; } })()
        : window.location.origin;

      url = origin + '/api/chat';
      body = JSON.stringify({
        provider: settings.provider,
        baseUrl: settings.baseUrl,
        apiKey: settings.apiKey,
        model: settings.model,
        messages: [
          { role: 'system', content: systemPrompt },
          ...conversationHistory
        ],
        max_tokens: 1000,
        temperature: 0.7
      });
    } else {
      url = `${settings.baseUrl}/chat/completions`;
      if (settings.provider === 'gemini' && settings.apiKey) url += `?key=${settings.apiKey}`;
      body = JSON.stringify({
        model: settings.model,
        messages: [
          { role: 'system', content: systemPrompt },
          ...conversationHistory
        ],
        max_tokens: 1000,
        temperature: 0.7
      });
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body
    });

    if (!response.ok) {
      const errJson = await response.json().catch(() => ({}));
      throw new Error(errJson.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || 'Sorry, could not generate a response.';

    removeThinking();
    conversationHistory.push({ role: 'assistant', content: reply });
    addMessage('ai', parseMarkdown(reply));

    // Auto-populate scheme cards from chat response
    updateSchemesFromChat(reply);

  } catch (err) {
    console.error(err);
    removeThinking();
    addMessage('ai', `⚠️ Error: ${err.message}<br>Please check your API settings and connection.`);
  }

  document.getElementById('send-btn').disabled = false;
}

function updateSchemesFromChat(replyText) {
  const lower = replyText.toLowerCase();
  const matched = [];
  SCHEME_DB.forEach(s => {
    const terms = [s.name.toLowerCase(), s.fullName.toLowerCase(), s.id];
    if (terms.some(t => lower.includes(t))) {
      matched.push(s);
    }
  });

  if (matched.length > 0) {
    const container = document.getElementById('scheme-cards');
    const placeholder = document.getElementById('schemes-placeholder');
    placeholder.classList.add('hidden');

    const catColorMap = { health:'cat-health', education:'cat-education', agriculture:'cat-agriculture', housing:'cat-housing', women:'cat-women', employment:'cat-employment', pension:'cat-pension' };
    const catEmoji = { health:'🏥', education:'📚', agriculture:'🌾', housing:'🏠', women:'👩', employment:'💼', pension:'🪙' };
    const T = TRANSLATIONS[currentLang];

    container.innerHTML = '';
    matched.forEach(s => {
      const div = document.createElement('div');
      div.className = 'scheme-card';
      const catClass = catColorMap[s.category] || 'cat-health';
      div.innerHTML = `
        <div class="scheme-card-header">
          <div class="scheme-category-badge ${catClass}">
            ${catEmoji[s.category] || '📋'} ${s.category.toUpperCase()}
          </div>
          <div class="scheme-name">${s.name}</div>
          <div class="scheme-ministry">${s.ministry}</div>
          <div class="match-badge">${s.match}% ${T['match'] || 'Match'}</div>
        </div>
        <div class="scheme-card-body">
          <div class="scheme-benefit">${s.benefit}</div>
          <div class="scheme-eligibility">👤 ${s.eligibility}</div>
          <div class="scheme-pros">${s.pros.map(p => `<span>✓</span>${p}<br>`).join('')}</div>
          ${s.portal ? `<a class="portal-link" href="${s.portal}" target="_blank">🔗 Official Portal ↗</a>` : ''}
        </div>
      `;
      div.onclick = (e) => { if (!e.target.closest('.portal-link')) showApplyGuide(s); };
      container.appendChild(div);
    });

    document.getElementById('schemes-dot').classList.remove('hidden');
    document.getElementById('apply-dot').classList.remove('hidden');
  }
}

// ============================================================
// MODEL BADGE
// ============================================================
function updateModelBadge() {
  const provMap = { gemini: '🟢 Gemini', custom: '⚡ Custom API' };
  document.getElementById('model-badge').textContent = provMap[aiSettings.provider] || '⚡ AI';
}

// ============================================================
// SETTINGS MODAL
// ============================================================
function openSettings() {
  document.getElementById('setting-provider').value = aiSettings.provider;
  document.getElementById('setting-base-url').value = aiSettings.baseUrl;
  document.getElementById('setting-api-key').value = aiSettings.apiKey;
  document.getElementById('setting-model').value = aiSettings.model;
  document.getElementById('settings-modal').classList.add('active');
}

function closeSettings() {
  document.getElementById('settings-modal').classList.remove('active');
}

function onProviderChange() {
  const p = document.getElementById('setting-provider').value;
  if (p === 'gemini') {
    document.getElementById('setting-base-url').value = 'https://generativelanguage.googleapis.com/v1beta/openai';
    document.getElementById('setting-model').value = 'gemini-2.5-flash-lite';
  } else {
    document.getElementById('setting-base-url').value = '';
    document.getElementById('setting-model').value = '';
  }
}

function saveSettings() {
  aiSettings.provider = document.getElementById('setting-provider').value;
  aiSettings.baseUrl = document.getElementById('setting-base-url').value;
  aiSettings.apiKey = document.getElementById('setting-api-key').value;
  aiSettings.model = document.getElementById('setting-model').value;
  localStorage.setItem('sahay_settings', JSON.stringify(aiSettings));
  updateModelBadge();
  closeSettings();
  alert('Settings saved!');
}

function loadSettings() {
  const saved = localStorage.getItem('sahay_settings');
  if (saved) {
    try { aiSettings = { ...aiSettings, ...JSON.parse(saved) }; } catch(e) {}
  }
}

// ============================================================
// INIT
// ============================================================
loadSettings();
setLang('en');
updateModelBadge();
</script>
</body>
</html>"""

# Inject API key into frontend
HTML_CONTENT = HTML_CONTENT.replace("apiKey: ''", f"apiKey: '{GEMINI_API_KEY}'")

# =========================================================================
# STARLETTE / ASGI PROXY (IDENTICAL TO ORIGINAL SKELETON)
# =========================================================================
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.endpoints import HTTPEndpoint


class StarletteProxyEndpoint(HTTPEndpoint):
    async def options(self, request):
        response = Response(status_code=204)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    async def post(self, request):
        try:
            body_bytes = await request.body()
            req_data = json.loads(body_bytes.decode('utf-8'))
        except Exception as e:
            resp = JSONResponse({"error": {"message": f"Invalid JSON body: {str(e)}"}}, status_code=400)
            resp.headers["Access-Control-Allow-Origin"] = "*"
            return resp

        provider = req_data.get('provider')
        base_url = req_data.get('baseUrl')
        api_key = req_data.get('apiKey')
        model = req_data.get('model')

        # Fallback to secure backend keys
        if not api_key:
            if provider == 'gemini':
                api_key = GEMINI_API_KEY
            elif provider == 'nvidia':
                api_key = NVIDIA_NIM_KEY
            elif provider == 'custom':
                api_key = CUSTOM_API_KEY

        is_test = request.url.path == "/api/test"

        # Use native Gemini generateContent API
        if provider == 'gemini' and not is_test:
            gemini_model = model
            if gemini_model.startswith('models/'):
                gemini_model = gemini_model[7:]
            if gemini_model == 'gemini-1.5-flash':
                gemini_model = 'gemini-2.5-flash-lite'
            dest_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent"
            if api_key:
                dest_url += f"?key={api_key}"
            method = 'POST'

            messages = req_data.get('messages', [])
            contents = []
            system_instruction = None
            for msg in messages:
                role = msg.get('role')
                content = msg.get('content')
                if role == 'system':
                    system_instruction = {"parts": [{"text": content}]}
                else:
                    contents.append({
                        "role": 'user' if role == 'user' else 'model',
                        "parts": [{"text": content}]
                    })

            req_body = json.dumps({
                "contents": contents,
                "systemInstruction": system_instruction,
                "tools": [{"google_search": {}}],
                "generationConfig": {
                    "maxOutputTokens": req_data.get('max_tokens', 1000),
                    "temperature": req_data.get('temperature', 0.7)
                }
            }).encode('utf-8')
        else:
            if is_test:
                dest_url = f"{base_url}/models"
                if provider == 'gemini' and api_key:
                    dest_url += f"?key={api_key}"
                method = 'GET'
                req_body = None
            else:
                dest_url = f"{base_url}/chat/completions"
                if provider == 'gemini' and api_key:
                    dest_url += f"?key={api_key}"
                method = 'POST'
                req_body = json.dumps({
                    "model": model,
                    "messages": req_data.get('messages', []),
                    "max_tokens": req_data.get('max_tokens', 1000),
                    "temperature": req_data.get('temperature', 0.7)
                }).encode('utf-8')

        req = urllib.request.Request(dest_url, data=req_body, method=method)
        req.add_header('Content-Type', 'application/json')
        if api_key and not (provider == 'gemini' and not is_test):
            req.add_header('Authorization', f'Bearer {api_key}')

        try:
            with urllib.request.urlopen(req) as response:
                res_data = response.read()

                if provider == 'gemini' and not is_test:
                    try:
                        gemini_res = json.loads(res_data.decode('utf-8'))
                        text = gemini_res['candidates'][0]['content']['parts'][0]['text']
                        openai_res = {
                            "choices": [{"message": {"role": "assistant", "content": text}}]
                        }
                        res_data = json.dumps(openai_res).encode('utf-8')
                    except Exception as e:
                        openai_res = {
                            "choices": [{"message": {"role": "assistant", "content": f"Error parsing response: {str(e)}"}}]
                        }
                        res_data = json.dumps(openai_res).encode('utf-8')

                resp = Response(res_data, media_type="application/json")
                resp.headers["Access-Control-Allow-Origin"] = "*"
                return resp

        except urllib.error.HTTPError as e:
            if is_test and e.code in [404, 405]:
                try:
                    dest_url = f"{base_url}/chat/completions"
                    if provider == 'gemini' and api_key:
                        dest_url += f"?key={api_key}"
                    req_body2 = json.dumps({
                        "model": model,
                        "messages": [{"role": "user", "content": "ping"}],
                        "max_tokens": 1
                    }).encode('utf-8')

                    req2 = urllib.request.Request(dest_url, data=req_body2, method='POST')
                    req2.add_header('Content-Type', 'application/json')
                    if api_key and not (provider == 'gemini'):
                        req2.add_header('Authorization', f'Bearer {api_key}')

                    with urllib.request.urlopen(req2) as resp2:
                        res_data2 = resp2.read()
                        resp = Response(res_data2, media_type="application/json")
                        resp.headers["Access-Control-Allow-Origin"] = "*"
                        return resp
                except Exception as e2:
                    resp = JSONResponse({"error": {"message": str(e2)}}, status_code=500)
                    resp.headers["Access-Control-Allow-Origin"] = "*"
                    return resp
            else:
                err_content = e.read() if hasattr(e, 'read') else str(e).encode('utf-8')
                resp = Response(err_content, status_code=e.code, media_type="application/json")
                resp.headers["Access-Control-Allow-Origin"] = "*"
                return resp
        except Exception as e:
            resp = JSONResponse({"error": {"message": str(e)}}, status_code=500)
            resp.headers["Access-Control-Allow-Origin"] = "*"
            return resp

    async def get(self, request):
        if request.url.path == "/api/test":
            resp = JSONResponse({"status": "running"})
            resp.headers["Access-Control-Allow-Origin"] = "*"
            return resp
        resp = Response("Method not allowed", status_code=405)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp


async def starlette_index_endpoint(request):
    return HTMLResponse(HTML_CONTENT)


# =========================================================================
# STREAMLIT / STANDALONE MODES (IDENTICAL STRUCTURE TO ORIGINAL)
# =========================================================================
is_streamlit = 'streamlit' in sys.modules

if is_streamlit:
    import streamlit as st
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    ctx = get_script_run_ctx()
    if ctx is not None:
        st.set_page_config(
            page_title="SAHAY - Government Scheme Finder",
            page_icon="🏛️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        st.components.v1.html(HTML_CONTENT, height=1050, scrolling=True)
else:
    import uvicorn

    def start_server():
        standalone_app = Starlette(routes=[
            Route("/", endpoint=starlette_index_endpoint, methods=["GET"]),
            Route("/index.html", endpoint=starlette_index_endpoint, methods=["GET"]),
            Route("/api/chat", endpoint=StarletteProxyEndpoint, methods=["POST", "OPTIONS"]),
            Route("/api/test", endpoint=StarletteProxyEndpoint, methods=["GET", "POST", "OPTIONS"])
        ])
        print("🏛️  SAHAY Government Scheme Finder running on http://localhost:8000")
        uvicorn.run(standalone_app, host="0.0.0.0", port=8000)

    start_server()
