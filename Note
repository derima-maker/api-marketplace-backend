<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Xiaomi Notes + AI</title>
  <!-- Puter.js for summarization -->
  <script src="https://js.puter.com/v2/"></script>
  <style>
    /* ---------- CSS VARIABLES (Light & Dark) ---------- */
    :root {
      --bg-body: #f5f7fa;
      --bg-card: #ffffff;
      --bg-header: rgba(255, 255, 255, 0.8);
      --bg-editor: #ffffff;
      --bg-toolbar: #ffffff;
      --bg-input: #f3f4f6;
      --text-main: #1f2937;
      --text-dim: #6b7280;
      --text-light: #9ca3af;
      --border-light: #e5e7eb;
      --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      --shadow-lg: 0 10px 25px -3px rgba(0, 0, 0, 0.1);
      --accent: #2563eb;
      --accent-hover: #1d4ed8;
      --radius: 16px;
      --transition: 0.25s ease;
      --modal-bg: rgba(0, 0, 0, 0.4);
      --modal-backdrop: rgba(0, 0, 0, 0.3);
    }

    [data-theme="dark"] {
      --bg-body: #0f172a;
      --bg-card: #1e293b;
      --bg-header: rgba(15, 23, 42, 0.85);
      --bg-editor: #1e293b;
      --bg-toolbar: #1e293b;
      --bg-input: #334155;
      --text-main: #f1f5f9;
      --text-dim: #94a3b8;
      --text-light: #64748b;
      --border-light: #334155;
      --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.6);
      --shadow-lg: 0 10px 25px -3px rgba(0, 0, 0, 0.7);
      --accent: #3b82f6;
      --accent-hover: #60a5fa;
      --modal-bg: rgba(0, 0, 0, 0.7);
      --modal-backdrop: rgba(0, 0, 0, 0.5);
    }

    /* ---------- RESET & BASE ---------- */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg-body);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
      transition: background var(--transition), color var(--transition);
    }

    button,
    select,
    input {
      font: inherit;
      background: none;
      border: none;
      outline: none;
      cursor: pointer;
    }

    ::-webkit-scrollbar {
      width: 4px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border-light);
      border-radius: 20px;
    }

    /* ---------- PAGE CONTAINERS ---------- */
    .page {
      display: none;
      flex-direction: column;
      height: 100vh;
      width: 100%;
      overflow: hidden;
      animation: fadeIn 0.25s ease;
    }

    .page.active {
      display: flex;
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(8px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    /* ---------- HOME PAGE ---------- */
    #home-page {
      background: var(--bg-body);
      padding: 24px 32px 32px 32px;
      transition: background var(--transition);
    }

    #home-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 32px;
      padding: 8px 0;
    }

    #home-header h1 {
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.5px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #home-header h1 span {
      background: var(--accent);
      color: white;
      font-size: 12px;
      font-weight: 600;
      padding: 2px 12px;
      border-radius: 100px;
      line-height: 20px;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    #search-input {
      background: var(--bg-input);
      padding: 10px 16px;
      border-radius: 12px;
      font-size: 14px;
      color: var(--text-main);
      width: 220px;
      border: 1px solid transparent;
      transition: 0.15s;
    }

    #search-input::placeholder {
      color: var(--text-light);
    }

    #search-input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    .icon-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      background: var(--bg-card);
      color: var(--text-main);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border-light);
      transition: 0.15s;
    }

    .icon-btn:hover {
      background: var(--bg-input);
      transform: scale(1.05);
    }

    /* Note Grid */
    .note-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 20px;
      flex: 1;
      overflow-y: auto;
      padding: 4px 0 80px 0;
      align-content: start;
    }

    .note-card {
      background: var(--bg-card);
      border-radius: var(--radius);
      padding: 20px 24px;
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border-light);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
      position: relative;
    }

    .note-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent);
    }

    .note-card-title {
      font-size: 17px;
      font-weight: 600;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 24px;
    }

    .note-card-preview {
      font-size: 14px;
      color: var(--text-dim);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      line-height: 1.5;
      flex: 1;
    }

    .note-card-meta {
      font-size: 12px;
      color: var(--text-light);
      margin-top: 8px;
      border-top: 1px solid var(--border-light);
      padding-top: 8px;
      display: flex;
      justify-content: space-between;
    }

    /* Delete button on card */
    .card-delete-btn {
      position: absolute;
      top: 12px;
      right: 14px;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: transparent;
      color: var(--text-light);
      font-size: 16px;
      font-weight: 300;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
      opacity: 0;
      border: 1px solid transparent;
    }

    .note-card:hover .card-delete-btn {
      opacity: 1;
    }

    .card-delete-btn:hover {
      background: #ef4444;
      color: white;
      border-color: #ef4444;
      transform: scale(1.1);
    }

    .note-empty {
      grid-column: 1 / -1;
      text-align: center;
      padding: 80px 20px;
      color: var(--text-dim);
    }

    .note-empty h3 {
      font-size: 20px;
      font-weight: 500;
      margin-bottom: 8px;
    }

    .note-empty p {
      font-size: 14px;
    }

    /* FAB */
    .fab {
      position: fixed;
      bottom: 32px;
      right: 32px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: var(--accent);
      color: white;
      font-size: 28px;
      font-weight: 300;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
    }

    .fab:hover {
      transform: scale(1.08);
      background: var(--accent-hover);
      box-shadow: 0 6px 24px rgba(37, 99, 235, 0.5);
    }

    /* ---------- EDITOR PAGE ---------- */
    #editor-page {
      background: var(--bg-body);
      padding: 0;
    }

    #editor-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 24px;
      background: var(--bg-header);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-light);
      flex-shrink: 0;
      flex-wrap: wrap;
    }

    #back-home-btn {
      font-size: 22px;
      padding: 4px 8px;
      border-radius: 8px;
      color: var(--text-main);
    }

    #back-home-btn:hover {
      background: var(--bg-input);
    }

    #editor-header #note-title {
      font-size: 22px;
      font-weight: 600;
      background: transparent;
      color: var(--text-main);
      padding: 4px 0;
      flex: 1;
      min-width: 120px;
      border-bottom: 2px solid transparent;
      transition: 0.15s;
    }

    #editor-header #note-title:focus {
      border-bottom-color: var(--accent);
    }

    #editor-header #note-title::placeholder {
      color: var(--text-light);
    }

    #editor-header #save-status {
      font-size: 12px;
      color: var(--text-light);
      white-space: nowrap;
    }

    /* ---------- COMPACT TOOLBAR ---------- */
    #toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 4px;
      padding: 6px 16px;
      background: var(--bg-toolbar);
      border-bottom: 1px solid var(--border-light);
      flex-shrink: 0;
      transition: background var(--transition);
      min-height: 48px;
      position: relative;
      z-index: 50;
    }

    #toolbar .group {
      display: flex;
      align-items: center;
      gap: 2px;
      padding: 0 6px;
      border-right: 1px solid var(--border-light);
    }

    #toolbar .group:last-child {
      border-right: none;
    }

    /* Always-visible buttons */
    #toolbar button {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      font-weight: 500;
      font-size: 13px;
      color: var(--text-dim);
      transition: all 0.1s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    #toolbar button:hover {
      background: var(--bg-input);
      color: var(--text-main);
    }

    #toolbar button.active {
      background: var(--accent);
      color: white;
    }

    /* Dropdown toggles */
    .dropdown-toggle {
      font-size: 16px !important;
      width: 32px;
      height: 32px;
    }

    /* Dropdown panels */
    .dropdown-group {
      position: relative;
    }

    .dropdown-panel {
      display: none;
      position: absolute;
      top: calc(100% + 8px);
      left: 0;
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: var(--shadow-lg);
      z-index: 100;
      min-width: 200px;
      backdrop-filter: blur(12px);
      flex-direction: column;
      gap: 6px;
    }

    .dropdown-panel.active {
      display: flex;
    }

    .dropdown-panel .panel-row {
      display: flex;
      align-items: center;
      gap: 2px;
      flex-wrap: wrap;
    }

    .dropdown-panel .panel-row:not(:last-child) {
      padding-bottom: 6px;
      border-bottom: 1px solid var(--border-light);
    }

    .dropdown-panel button {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      font-weight: 500;
      font-size: 13px;
      color: var(--text-dim);
      transition: all 0.1s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
    }

    .dropdown-panel button:hover {
      background: var(--bg-input);
      color: var(--text-main);
    }

    /* ---------- HORIZONTAL COLOR PALETTE ---------- */
    .color-palette {
      display: flex;
      gap: 6px;
      flex-wrap: nowrap;
      padding: 4px 0;
    }

    .color-swatch {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      border: 2px solid transparent;
      cursor: pointer;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }

    .color-swatch:hover {
      transform: scale(1.15);
      border-color: var(--accent);
    }

    .color-swatch.active {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--bg-card), 0 0 0 4px var(--accent);
    }

    /* Right-aligned color dropdown */
    .color-dropdown-group {
      position: relative;
      margin-left: auto;
    }

    .color-dropdown-group .dropdown-panel {
      left: auto;
      right: 0;
      min-width: 180px;
      padding: 10px 14px;
    }

    /* Selects in toolbar */
    #toolbar select {
      background: var(--bg-input);
      padding: 4px 10px 4px 8px;
      border-radius: 8px;
      font-size: 12px;
      height: 30px;
      border: 1px solid var(--border-light);
      cursor: pointer;
      color: var(--text-main);
      transition: 0.1s;
      max-width: 110px;
    }

    #toolbar select:hover {
      border-color: var(--accent);
    }

    /* AI buttons – always visible, compact */
    .ai-btn {
      background: var(--bg-input) !important;
      color: var(--accent) !important;
      font-size: 12px !important;
      border-radius: 8px !important;
      padding: 0 10px !important;
      width: auto !important;
      gap: 4px;
      font-weight: 500 !important;
      height: 30px !important;
      line-height: 30px !important;
    }

    .ai-btn:hover {
      background: var(--accent) !important;
      color: white !important;
    }

    /* Editor Content */
    #editor-content-wrap {
      flex: 1;
      overflow: auto;
      padding: 24px 32px 40px 32px;
      background: var(--bg-body);
    }

    #editor-content {
      background: var(--bg-editor);
      padding: 48px 56px;
      min-height: 100%;
      outline: none;
      font-size: 15px;
      line-height: 1.7;
      color: var(--text-main);
      border-radius: var(--radius);
      box-shadow: var(--shadow-sm);
      transition: background var(--transition), color var(--transition), box-shadow var(--transition);
      max-width: 100%;
      margin: 0 auto;
      border: 1px solid var(--border-light);
    }

    #editor-content:focus {
      box-shadow: var(--shadow-md);
    }

    #editor-content blockquote {
      border-left: 3px solid var(--accent);
      padding-left: 20px;
      margin: 12px 0;
      color: var(--text-dim);
      background: var(--bg-input);
      padding: 12px 20px;
      border-radius: 0 8px 8px 0;
    }

    #editor-content ul,
    #editor-content ol {
      padding-left: 28px;
      margin: 8px 0;
    }

    #editor-content p {
      margin: 0 0 8px 0;
    }

    /* Editor Footer */
    #editor-footer {
      display: flex;
      justify-content: space-between;
      padding: 10px 24px;
      background: var(--bg-header);
      backdrop-filter: blur(8px);
      border-top: 1px solid var(--border-light);
      font-size: 12px;
      color: var(--text-light);
      flex-shrink: 0;
    }

    #editor-footer span {
      display: flex;
      gap: 20px;
    }

    /* ---------- MODAL (Language Picker) ---------- */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: var(--modal-backdrop);
      backdrop-filter: blur(8px);
      z-index: 1000;
      justify-content: center;
      align-items: center;
      animation: fadeIn 0.2s ease;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-content {
      background: var(--bg-card);
      border-radius: var(--radius);
      padding: 32px 36px;
      max-width: 480px;
      width: 90%;
      max-height: 80vh;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border-light);
      display: flex;
      flex-direction: column;
      animation: scaleIn 0.2s ease;
    }

    @keyframes scaleIn {
      from {
        transform: scale(0.95);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }

    .modal-title {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 16px;
      color: var(--text-main);
    }

    .modal-search {
      background: var(--bg-input);
      padding: 10px 14px;
      border-radius: 10px;
      font-size: 14px;
      color: var(--text-main);
      width: 100%;
      border: 1px solid transparent;
      transition: 0.15s;
      margin-bottom: 12px;
    }

    .modal-search:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }

    .modal-search::placeholder {
      color: var(--text-light);
    }

    .language-list {
      flex: 1;
      overflow-y: auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
      padding-right: 4px;
    }

    .language-item {
      padding: 8px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.1s ease;
      font-size: 14px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .language-item:hover {
      background: var(--bg-input);
    }

    .language-item .lang-code {
      font-size: 11px;
      color: var(--text-light);
      font-weight: 400;
    }

    .modal-close-btn {
      margin-top: 12px;
      padding: 10px;
      border-radius: 10px;
      background: var(--bg-input);
      color: var(--text-main);
      font-size: 14px;
      font-weight: 500;
      transition: 0.15s;
      width: 100%;
    }

    .modal-close-btn:hover {
      background: var(--border-light);
    }

    /* ---------- LOADING OVERLAY ---------- */
    #ai-loading {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(6px);
      z-index: 999;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      font-size: 18px;
      color: white;
      font-weight: 500;
    }

    #ai-loading.active {
      display: flex;
    }

    .spinner {
      width: 40px;
      height: 40px;
      border: 4px solid rgba(255, 255, 255, 0.2);
      border-top-color: white;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
      margin-bottom: 16px;
    }

    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }

    #ai-loading .status-text {
      animation: pulse 1.2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%,
      100% {
        opacity: 1;
      }
      50% {
        opacity: 0.4;
      }
    }

    /* ---------- RESPONSIVE ---------- */
    @media (max-width: 640px) {
      #home-page {
        padding: 16px;
      }

      #home-header h1 {
        font-size: 22px;
      }

      #search-input {
        width: 140px;
      }

      .note-grid {
        grid-template-columns: 1fr;
        gap: 12px;
      }

      #editor-content {
        padding: 24px 20px;
        border-radius: 12px;
      }

      #editor-header {
        padding: 8px 16px;
      }

      #editor-header #note-title {
        font-size: 18px;
      }

      #toolbar {
        padding: 4px 8px;
        gap: 2px;
      }

      #toolbar .group {
        padding: 0 3px;
      }

      #editor-content-wrap {
        padding: 12px;
      }

      .fab {
        bottom: 20px;
        right: 20px;
        width: 48px;
        height: 48px;
        font-size: 24px;
      }

      .dropdown-panel {
        left: -40px;
        min-width: 180px;
      }

      #toolbar select {
        max-width: 80px;
        font-size: 11px;
        padding: 2px 6px;
      }

      .ai-btn {
        font-size: 10px !important;
        padding: 0 6px !important;
        height: 26px !important;
        line-height: 26px !important;
      }

      .modal-content {
        padding: 24px 20px;
        max-width: 100%;
      }

      .language-list {
        grid-template-columns: 1fr;
      }

      .color-dropdown-group .dropdown-panel {
        right: -10px;
        min-width: 160px;
      }

      .color-swatch {
        width: 24px;
        height: 24px;
      }
    }

    @media (max-width: 480px) {
      #home-header {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
      }

      .header-controls {
        justify-content: space-between;
      }

      #search-input {
        width: 100%;
      }

      .dropdown-panel {
        left: -80px;
        min-width: 160px;
      }

      .color-dropdown-group .dropdown-panel {
        right: -20px;
      }
    }
  </style>
</head>
<body>

  <!-- ================================================================
  AI LOADING OVERLAY
  ================================================================ -->
  <div id="ai-loading">
    <div class="spinner"></div>
    <div class="status-text">AI is thinking<span class="dots">...</span></div>
  </div>

  <!-- ================================================================
  LANGUAGE SELECTOR MODAL
  ================================================================ -->
  <div class="modal-overlay" id="language-modal">
    <div class="modal-content">
      <div class="modal-title">🌐 Choose Language</div>
      <input class="modal-search" id="lang-search" placeholder="Search languages..." type="text" />
      <div class="language-list" id="language-list"></div>
      <button class="modal-close-btn" id="modal-close-btn">Cancel</button>
    </div>
  </div>

  <!-- ================================================================
  HOME PAGE
  ================================================================ -->
  <div id="home-page" class="page active">
    <header id="home-header">
      <h1>
        📝 Notes
        <span>AI</span>
      </h1>
      <div class="header-controls">
        <input id="search-input" placeholder="Search notes..." type="text" />
        <button id="theme-toggle" class="icon-btn" title="Toggle theme">🌙</button>
      </div>
    </header>
    <div id="note-grid" class="note-grid"></div>
    <button id="new-note-fab" class="fab" title="New Project">＋</button>
  </div>

  <!-- ================================================================
  EDITOR PAGE
  ================================================================ -->
  <div id="editor-page" class="page">
    <!-- Editor Header -->
    <header id="editor-header">
      <button id="back-home-btn" class="icon-btn" title="Back to home">←</button>
      <input id="note-title" placeholder="Untitled Note" type="text" />
      <span id="save-status">💾 All changes saved</span>
    </header>

    <!-- COMPACT TOOLBAR -->
    <div id="toolbar">
      <!-- Group 1: Text Style (always visible) -->
      <div class="group">
        <button data-cmd="bold" title="Bold"><b>B</b></button>
        <button data-cmd="italic" title="Italic"><i>I</i></button>
        <button data-cmd="underline" title="Underline"><u>U</u></button>
        <button data-cmd="strikeThrough" title="Strikethrough"><s>S</s></button>
      </div>

      <!-- Group 2: Font & Size (always visible) -->
      <div class="group">
        <select id="font-family">
          <option value="Inter, system-ui">System</option>
          <option value="Arial">Arial</option>
          <option value="Times New Roman">Times New Roman</option>
          <option value="Georgia">Georgia</option>
          <option value="Courier New">Courier New</option>
          <option value="Segoe UI">Segoe UI</option>
          <option value="Verdana">Verdana</option>
        </select>
        <select id="font-size">
          <option value="8">8</option><option value="9">9</option><option value="10">10</option>
          <option value="11">11</option><option value="12">12</option>
          <option value="14">14</option><option value="16" selected>16</option>
          <option value="18">18</option><option value="20">20</option>
          <option value="24">24</option><option value="28">28</option>
          <option value="32">32</option><option value="36">36</option>
          <option value="48">48</option><option value="72">72</option>
        </select>
      </div>

      <!-- Group 3: Paragraph & Structure (dropdown) -->
      <div class="group dropdown-group">
        <button class="dropdown-toggle" data-target="dropdown-para" title="Paragraph & Structure">📐</button>
        <div class="dropdown-panel" id="dropdown-para">
          <div class="panel-row">
            <button data-cmd="justifyLeft" title="Align Left">≡</button>
            <button data-cmd="justifyCenter" title="Center">☰</button>
            <button data-cmd="justifyRight" title="Align Right">≢</button>
            <button data-cmd="justifyFull" title="Justify">⬌</button>
          </div>
          <div class="panel-row">
            <button data-cmd="insertUnorderedList" title="Bullet List">•</button>
            <button data-cmd="insertOrderedList" title="Numbered List">1.</button>
            <button data-cmd="indent" title="Indent">→</button>
            <button data-cmd="outdent" title="Outdent">←</button>
          </div>
          <div class="panel-row">
            <button data-cmd="formatBlock" data-value="blockquote" title="Blockquote">“</button>
            <button data-cmd="removeFormat" title="Clear Formatting">🧹</button>
          </div>
        </div>
      </div>

      <!-- Group 4: History (always visible) -->
      <div class="group">
        <button id="undo-btn" title="Undo">↩</button>
        <button id="redo-btn" title="Redo">↪</button>
      </div>

      <!-- Group 5: AI Tools (always visible) -->
      <div class="group">
        <button class="ai-btn" id="ai-summarize" title="Summarize selected text">✨ Summarize</button>
        <button class="ai-btn" id="ai-fix" title="Fix grammar & spelling">🔧 Fix</button>
        <button class="ai-btn" id="ai-translate" title="Translate selected text">🌐 Translate</button>
        <button class="ai-btn" id="ai-generate" title="Generate text from prompt">✏️ Generate</button>
      </div>

      <!-- Group 6: Color Palette (right-aligned) -->
      <div class="group color-dropdown-group">
        <button class="dropdown-toggle" data-target="dropdown-colors" title="Text Color">🎨</button>
        <div class="dropdown-panel" id="dropdown-colors">
          <div class="panel-row">
            <div class="color-palette" id="color-palette"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div id="editor-content-wrap">
      <div id="editor-content" contenteditable="true" spellcheck="true"></div>
    </div>

    <!-- Footer -->
    <div id="editor-footer">
      <span id="word-char-count">Words: 0  |  Characters: 0</span>
      <span id="editor-save-status">💾 All changes saved</span>
    </div>
  </div>

  <!-- ================================================================
  JAVASCRIPT
  ================================================================ -->
  <script>
    // ============================================================
    //  LANGUAGE LIST (expanded)
    // ============================================================
    const LANGUAGES = [
      { code: 'es', name: 'Spanish' },
      { code: 'fr', name: 'French' },
      { code: 'de', name: 'German' },
      { code: 'it', name: 'Italian' },
      { code: 'pt', name: 'Portuguese' },
      { code: 'ru', name: 'Russian' },
      { code: 'ja', name: 'Japanese' },
      { code: 'zh', name: 'Chinese (Simplified)' },
      { code: 'ko', name: 'Korean' },
      { code: 'ar', name: 'Arabic' },
      { code: 'hi', name: 'Hindi' },
      { code: 'nl', name: 'Dutch' },
      { code: 'pl', name: 'Polish' },
      { code: 'uk', name: 'Ukrainian' },
      { code: 'sv', name: 'Swedish' },
      { code: 'tr', name: 'Turkish' },
      { code: 'fa', name: 'Persian' },
      { code: 'he', name: 'Hebrew' },
      { code: 'th', name: 'Thai' },
      { code: 'vi', name: 'Vietnamese' },
      { code: 'id', name: 'Indonesian' },
      { code: 'ms', name: 'Malay' },
      { code: 'ro', name: 'Romanian' },
      { code: 'hu', name: 'Hungarian' },
      { code: 'cs', name: 'Czech' },
      { code: 'el', name: 'Greek' },
      { code: 'no', name: 'Norwegian' },
      { code: 'da', name: 'Danish' },
      { code: 'fi', name: 'Finnish' },
      { code: 'bg', name: 'Bulgarian' },
      { code: 'sr', name: 'Serbian' },
      { code: 'hr', name: 'Croatian' },
      { code: 'sk', name: 'Slovak' },
      { code: 'sl', name: 'Slovenian' },
      { code: 'lt', name: 'Lithuanian' },
      { code: 'lv', name: 'Latvian' },
      { code: 'et', name: 'Estonian' },
      { code: 'is', name: 'Icelandic' },
      { code: 'ga', name: 'Irish' },
      { code: 'cy', name: 'Welsh' },
      { code: 'ml', name: 'Malayalam' },
      { code: 'ta', name: 'Tamil' },
      { code: 'te', name: 'Telugu' },
      { code: 'kn', name: 'Kannada' },
      { code: 'bn', name: 'Bengali' },
      { code: 'ur', name: 'Urdu' },
      { code: 'pa', name: 'Punjabi' },
      { code: 'ne', name: 'Nepali' },
      { code: 'si', name: 'Sinhala' },
      { code: 'my', name: 'Burmese' },
      { code: 'km', name: 'Khmer' },
      { code: 'lo', name: 'Lao' },
      { code: 'sw', name: 'Swahili' },
      { code: 'yo', name: 'Yoruba' },
      { code: 'ig', name: 'Igbo' },
      { code: 'ha', name: 'Hausa' },
      { code: 'zu', name: 'Zulu' },
      { code: 'af', name: 'Afrikaans' },
      { code: 'sq', name: 'Albanian' },
      { code: 'hy', name: 'Armenian' },
      { code: 'az', name: 'Azerbaijani' },
      { code: 'eu', name: 'Basque' },
      { code: 'be', name: 'Belarusian' },
      { code: 'bs', name: 'Bosnian' },
      { code: 'ca', name: 'Catalan' },
      { code: 'eo', name: 'Esperanto' },
      { code: 'gl', name: 'Galician' },
      { code: 'ka', name: 'Georgian' },
      { code: 'ht', name: 'Haitian Creole' },
      { code: 'haw', name: 'Hawaiian' },
      { code: 'ji', name: 'Yiddish' },
      { code: 'fy', name: 'Frisian' },
      { code: 'gd', name: 'Scottish Gaelic' },
      { code: 'lb', name: 'Luxembourgish' },
      { code: 'mk', name: 'Macedonian' },
      { code: 'mt', name: 'Maltese' },
      { code: 'mn', name: 'Mongolian' },
      { code: 'ps', name: 'Pashto' },
      { code: 'so', name: 'Somali' },
      { code: 'tl', name: 'Tagalog' },
      { code: 'tg', name: 'Tajik' },
      { code: 'uz', name: 'Uzbek' },
    ];

    // ============================================================
    //  COLOR PALETTE
    // ============================================================
    const COLORS = [
      '#1f2937', // Dark
      '#ef4444', // Red
      '#f59e0b', // Amber
      '#22c55e', // Green
      '#3b82f6', // Blue
      '#8b5cf6', // Purple
      '#ec4899', // Pink
      '#14b8a6', // Teal
      '#f97316', // Orange
      '#84cc16', // Lime
      '#06b6d4', // Cyan
      '#a855f7', // Violet
    ];

    // ============================================================
    //  STATE
    // ============================================================
    const state = {
      notes: [],
      activeId: null,
      nextId: 1,
      searchTerm: '',
      history: {},
      isRestoring: false,
      saveTimeout: null,
      theme: 'light',
    };

    // DOM refs
    const $ = (id) => document.getElementById(id);
    const homePage = $('home-page');
    const editorPage = $('editor-page');
    const noteGrid = $('note-grid');
    const searchInput = $('search-input');
    const titleInput = $('note-title');
    const contentDiv = $('editor-content');
    const wordCount = $('word-char-count');
    const saveStatus = $('save-status');
    const editorSaveStatus = $('editor-save-status');
    const newNoteBtn = $('new-note-fab');
    const backHomeBtn = $('back-home-btn');
    const themeToggle = $('theme-toggle');
    const fontSizeSelect = $('font-size');
    const fontFamilySelect = $('font-family');
    const undoBtn = $('undo-btn');
    const redoBtn = $('redo-btn');
    const loadingOverlay = $('ai-loading');
    const loadingStatus = loadingOverlay.querySelector('.status-text');
    const languageModal = $('language-modal');
    const languageList = $('language-list');
    const langSearch = $('lang-search');
    const modalCloseBtn = $('modal-close-btn');
    const colorPalette = $('color-palette');

    // ============================================================
    //  THEME
    // ============================================================
    function setTheme(theme) {
      state.theme = theme;
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('notes_theme', theme);
      themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    function toggleTheme() {
      setTheme(state.theme === 'light' ? 'dark' : 'light');
    }

    const savedTheme = localStorage.getItem('notes_theme') || 'light';
    setTheme(savedTheme);
    themeToggle.addEventListener('click', toggleTheme);

    // ============================================================
    //  COLOR PALETTE SETUP
    // ============================================================
    function setupColorPalette() {
      colorPalette.innerHTML = '';
      COLORS.forEach(color => {
        const swatch = document.createElement('div');
        swatch.className = 'color-swatch';
        swatch.style.background = color;
        swatch.dataset.color = color;
        swatch.addEventListener('click', (e) => {
          e.stopPropagation();
          document.execCommand('foreColor', false, color);
          contentDiv.focus();
          autoSave();
          document.getElementById('dropdown-colors').classList.remove('active');
        });
        colorPalette.appendChild(swatch);
      });
    }
    setupColorPalette();

    // ============================================================
    //  DROPDOWN TOGGLES
    // ============================================================
    document.querySelectorAll('.dropdown-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const targetId = btn.dataset.target;
        const panel = document.getElementById(targetId);
        document.querySelectorAll('.dropdown-panel').forEach(p => {
          if (p.id !== targetId) p.classList.remove('active');
        });
        panel.classList.toggle('active');
      });
    });

    document.addEventListener('click', () => {
      document.querySelectorAll('.dropdown-panel').forEach(p => p.classList.remove('active'));
    });

    document.querySelectorAll('.dropdown-panel').forEach(panel => {
      panel.addEventListener('click', (e) => e.stopPropagation());
    });

    // ============================================================
    //  LANGUAGE MODAL
    // ============================================================
    let selectedLanguage = null;
    let translateResolve = null;

    function showLanguagePicker() {
      return new Promise((resolve) => {
        selectedLanguage = null;
        translateResolve = resolve;
        languageModal.classList.add('active');
        renderLanguages('');
        langSearch.value = '';
        langSearch.focus();
      });
    }

    function renderLanguages(filter) {
      const query = filter.toLowerCase().trim();
      const filtered = LANGUAGES.filter(lang =>
        lang.name.toLowerCase().includes(query) ||
        lang.code.toLowerCase().includes(query)
      );
      languageList.innerHTML = '';
      filtered.forEach(lang => {
        const item = document.createElement('div');
        item.className = 'language-item';
        item.innerHTML = `${lang.name} <span class="lang-code">${lang.code}</span>`;
        item.addEventListener('click', () => {
          selectedLanguage = lang.code;
          languageModal.classList.remove('active');
          if (translateResolve) {
            translateResolve(lang.code);
            translateResolve = null;
          }
        });
        languageList.appendChild(item);
      });
    }

    langSearch.addEventListener('input', (e) => {
      renderLanguages(e.target.value);
    });

    modalCloseBtn.addEventListener('click', () => {
      languageModal.classList.remove('active');
      if (translateResolve) {
        translateResolve(null);
        translateResolve = null;
      }
    });

    languageModal.addEventListener('click', (e) => {
      if (e.target === languageModal) {
        languageModal.classList.remove('active');
        if (translateResolve) {
          translateResolve(null);
          translateResolve = null;
        }
      }
    });

    // ============================================================
    //  NAVIGATION
    // ============================================================
    function showHome() {
      homePage.classList.add('active');
      editorPage.classList.remove('active');
      renderNoteGrid();
    }

    function showEditor(noteId) {
      homePage.classList.remove('active');
      editorPage.classList.add('active');
      loadNote(noteId);
      setTimeout(() => titleInput.focus(), 100);
    }

    backHomeBtn.addEventListener('click', () => {
      saveCurrentNote();
      showHome();
    });

    // ============================================================
    //  STORAGE
    // ============================================================
    function loadData() {
      try {
        const raw = localStorage.getItem('notepad_data');
        if (raw) {
          const data = JSON.parse(raw);
          state.notes = data.notes || [];
          state.nextId = data.nextId || 1;
          state.activeId = data.activeId || null;
          state.notes.forEach(n => {
            if (!state.history[n.id]) {
              state.history[n.id] = { stack: [n.content || ''], index: 0 };
            }
          });
          if (state.activeId && !state.notes.find(n => n.id === state.activeId)) {
            state.activeId = null;
          }
        }
      } catch (e) { console.warn('Load error', e); }
      if (!state.notes.length) createNewNote();
      if (!state.activeId) state.activeId = state.notes[0]?.id || null;
    }

    function saveData() {
      const data = {
        notes: state.notes,
        nextId: state.nextId,
        activeId: state.activeId,
      };
      localStorage.setItem('notepad_data', JSON.stringify(data));
    }

    function autoSave() {
      clearTimeout(state.saveTimeout);
      state.saveTimeout = setTimeout(() => {
        saveCurrentNote();
        saveData();
        const msg = '💾 All changes saved';
        saveStatus.textContent = msg;
        editorSaveStatus.textContent = msg;
      }, 400);
    }

    function saveCurrentNote() {
      if (!state.activeId) return;
      const note = state.notes.find(n => n.id === state.activeId);
      if (!note) return;
      note.title = titleInput.value.trim() || 'Untitled';
      note.content = contentDiv.innerHTML;
      note.updatedAt = Date.now();
      if (!state.history[note.id]) {
        state.history[note.id] = { stack: [note.content], index: 0 };
      }
      const hist = state.history[note.id];
      const last = hist.stack[hist.index];
      if (last !== note.content) {
        hist.stack = hist.stack.slice(0, hist.index + 1);
        hist.stack.push(note.content);
        hist.index++;
        if (hist.stack.length > 50) {
          hist.stack.shift();
          hist.index--;
        }
      }
      updateWordCount();
      renderNoteGrid();
    }

    // ============================================================
    //  NOTES CRUD
    // ============================================================
    function createNewNote() {
      const id = state.nextId++;
      const note = {
        id,
        title: 'Untitled',
        content: '<p>Start writing...</p>',
        createdAt: Date.now(),
        updatedAt: Date.now(),
      };
      state.notes.push(note);
      state.history[id] = { stack: [note.content], index: 0 };
      state.activeId = id;
      saveData();
      showEditor(id);
      autoSave();
    }

    function deleteNote(id) {
      if (!confirm('Delete this note?')) return;
      state.notes = state.notes.filter(n => n.id !== id);
      delete state.history[id];
      if (state.activeId === id) {
        state.activeId = state.notes[0]?.id || null;
      }
      saveData();
      if (state.activeId) {
        loadNote(state.activeId);
      } else {
        createNewNote();
      }
      renderNoteGrid();
    }

    function loadNote(id) {
      const note = state.notes.find(n => n.id === id);
      if (!note) return;
      state.activeId = id;
      state.isRestoring = true;
      titleInput.value = note.title;
      contentDiv.innerHTML = note.content;
      if (!state.history[id]) {
        state.history[id] = { stack: [note.content], index: 0 };
      }
      const hist = state.history[id];
      if (hist.stack.length === 0 || hist.stack[hist.index] !== note.content) {
        hist.stack.push(note.content);
        hist.index = hist.stack.length - 1;
      }
      updateWordCount();
      state.isRestoring = false;
      renderNoteGrid();
    }

    function getActiveNote() {
      return state.notes.find(n => n.id === state.activeId);
    }

    // ============================================================
    //  RENDER: HOME GRID
    // ============================================================
    function renderNoteGrid() {
      const term = state.searchTerm.toLowerCase().trim();
      let filtered = state.notes.filter(n => {
        if (term && !n.title.toLowerCase().includes(term) && !n.content.toLowerCase().includes(term)) return false;
        return true;
      });
      filtered.sort((a, b) => b.updatedAt - a.updatedAt);

      noteGrid.innerHTML = '';
      if (!filtered.length) {
        noteGrid.innerHTML = `
          <div class="note-empty">
            <h3>📭 No notes found</h3>
            <p>Tap the + button to create a new project.</p>
          </div>
        `;
        return;
      }
      filtered.forEach(n => {
        const card = document.createElement('div');
        card.className = 'note-card';

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'card-delete-btn';
        deleteBtn.textContent = '×';
        deleteBtn.title = 'Delete note';
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteNote(n.id);
        });
        card.appendChild(deleteBtn);

        const title = document.createElement('div');
        title.className = 'note-card-title';
        title.textContent = n.title || 'Untitled';

        const preview = document.createElement('div');
        preview.className = 'note-card-preview';
        const text = contentDivText(n.content);
        preview.textContent = text || 'Empty note';

        const meta = document.createElement('div');
        meta.className = 'note-card-meta';
        const date = new Date(n.updatedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        meta.innerHTML = `<span>${date}</span><span>${n.content.length > 50 ? '📄' : '📝'}</span>`;

        card.appendChild(title);
        card.appendChild(preview);
        card.appendChild(meta);

        card.addEventListener('click', () => {
          saveCurrentNote();
          showEditor(n.id);
        });

        noteGrid.appendChild(card);
      });
    }

    function contentDivText(html) {
      const tmp = document.createElement('div');
      tmp.innerHTML = html;
      return tmp.textContent || tmp.innerText || '';
    }

    // ============================================================
    //  WORD COUNT
    // ============================================================
    function updateWordCount() {
      const text = contentDiv.innerText || '';
      const words = text.trim() ? text.trim().split(/\s+/).length : 0;
      const chars = text.length;
      wordCount.textContent = `Words: ${words}  |  Characters: ${chars}`;
    }

    // ============================================================
    //  TOOLBAR COMMANDS
    // ============================================================
    function exec(cmd, value = null) {
      document.execCommand(cmd, false, value);
      contentDiv.focus();
      autoSave();
      updateWordCount();
    }

    document.querySelectorAll('#toolbar button[data-cmd]').forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.dataset.cmd;
        const val = btn.dataset.value || null;
        if (cmd === 'createLink') {
          const url = prompt('Enter URL:', 'https://');
          if (url) exec(cmd, url);
        } else {
          exec(cmd, val);
        }
      });
    });

    fontFamilySelect.addEventListener('change', () => {
      exec('fontName', fontFamilySelect.value);
    });

    fontSizeSelect.addEventListener('change', () => {
      const size = fontSizeSelect.value;
      const sel = window.getSelection();
      if (!sel.rangeCount || sel.isCollapsed) return;
      const range = sel.getRangeAt(0);
      const fragment = range.extractContents();
      const span = document.createElement('span');
      span.style.fontSize = size + 'px';
      span.appendChild(fragment);
      range.insertNode(span);
      range.selectNodeContents(span);
      sel.removeAllRanges();
      sel.addRange(range);
      contentDiv.focus();
      autoSave();
      updateWordCount();
    });

    function undo() {
      const note = getActiveNote();
      if (!note) return;
      const hist = state.history[note.id];
      if (!hist || hist.index <= 0) return;
      hist.index--;
      state.isRestoring = true;
      contentDiv.innerHTML = hist.stack[hist.index];
      state.isRestoring = false;
      autoSave();
      updateWordCount();
    }

    function redo() {
      const note = getActiveNote();
      if (!note) return;
      const hist = state.history[note.id];
      if (!hist || hist.index >= hist.stack.length - 1) return;
      hist.index++;
      state.isRestoring = true;
      contentDiv.innerHTML = hist.stack[hist.index];
      state.isRestoring = false;
      autoSave();
      updateWordCount();
    }

    undoBtn.addEventListener('click', undo);
    redoBtn.addEventListener('click', redo);

    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        if (e.shiftKey) { e.preventDefault();
          redo(); } else { e.preventDefault();
          undo(); }
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 'y') {
        e.preventDefault();
        redo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveCurrentNote();
        saveData();
        const msg = '💾 Saved manually';
        saveStatus.textContent = msg;
        editorSaveStatus.textContent = msg;
      }
    });

    contentDiv.addEventListener('input', () => {
      if (state.isRestoring) return;
      autoSave();
      updateWordCount();
    });

    contentDiv.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') autoSave();
    });

    titleInput.addEventListener('input', () => {
      autoSave();
      renderNoteGrid();
    });

    searchInput.addEventListener('input', () => {
      state.searchTerm = searchInput.value;
      renderNoteGrid();
    });

    newNoteBtn.addEventListener('click', createNewNote);

    // ============================================================
    //  FREE AI FUNCTIONS – UPDATED
    // ============================================================

    // Helper: truncate text to avoid API limits
    function truncateText(text, maxLength = 5000) {
      if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
      }
      return text;
    }

    // ----- 1. SUMMARIZE (Puter.js) -----
    async function summarizeWithPuter(text) {
      try {
        // Check if Puter is available
        if (typeof puter === 'undefined') {
          throw new Error('Puter.js library not loaded.');
        }
        const response = await puter.ai.chat({
          messages: [
            {
              role: 'system',
              content: 'You are a helpful assistant that summarizes text concisely. Return only the summary, nothing else.'
            },
            {
              role: 'user',
              content: `Summarize the following text concisely in 2-3 sentences:\n\n${truncateText(text, 3000)}`
            }
          ],
          model: 'gpt-4o-mini' // Use a capable free model
        });
        // Puter returns an object with 'content' or 'message' – check
        const summary = response.content || response.message || response;
        if (typeof summary === 'string' && summary.trim().length > 0) {
          return summary.trim();
        }
        throw new Error('Puter returned empty or invalid summary.');
      } catch (err) {
        console.warn('Puter.js failed:', err.message);
        // Fallback to Pollinations
        return await summarizeFallback(text);
      }
    }

    // Fallback summarizer (Pollinations)
    async function summarizeFallback(text) {
      const prompt = `Summarize this text concisely in 2-3 sentences:\n\n${truncateText(text, 2000)}`;
      const url = `https://text.pollinations.ai/${encodeURIComponent(prompt)}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Fallback summary error: ${response.status}`);
      let result = await response.text();
      if (result.includes('<html') || result.trim().length === 0) {
        throw new Error('Fallback summary returned invalid content.');
      }
      // Trim to first 3 sentences if too long
      const sentences = result.match(/[^.!?]+[.!?]+/g) || [result];
      if (sentences.length > 3) {
        result = sentences.slice(0, 3).join(' ');
      }
      return result.trim();
    }

    // ----- 2. GENERATE (DevToolBox AI) -----
    async function generateWithDevToolBox(instruction) {
      // Use DevToolBox AI free endpoint (no key)
      const url = `https://api.devtoolbox.com/ai/generate?prompt=${encodeURIComponent(instruction)}&length=200`;
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`DevToolBox error: ${response.status}`);
        const data = await response.json();
        // Expected response: { generated: "...", status: "success" } or similar
        if (data.generated && typeof data.generated === 'string') {
          return data.generated.trim();
        }
        // If response is plain text
        if (typeof data === 'string' && data.trim().length > 0) {
          return data.trim();
        }
        throw new Error('Unexpected DevToolBox response format.');
      } catch (err) {
        console.warn('DevToolBox failed:', err.message);
        // Fallback to Pollinations
        return await generateFallback(instruction);
      }
    }

    // Fallback generator (Pollinations)
    async function generateFallback(instruction) {
      const prompt = `Generate content based on this request: "${instruction}". Return only the generated text.`;
      const url = `https://text.pollinations.ai/${encodeURIComponent(truncateText(prompt, 2000))}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Fallback generate error: ${response.status}`);
      const result = await response.text();
      if (result.includes('<html') || result.trim().length === 0) {
        throw new Error('Fallback generate returned invalid content.');
      }
      return result.trim();
    }

    // ----- 3. TRANSLATE (LibreTranslate + MyMemory fallback) -----
    async function translateText(text, targetLang) {
      // LibreTranslate with auto-detect
      try {
        const url = 'https://libretranslate.com/translate';
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            q: truncateText(text, 5000),
            source: 'auto',
            target: targetLang,
            format: 'text',
          }),
        });
        if (!response.ok) throw new Error(`LibreTranslate error: ${response.status}`);
        const data = await response.json();
        if (data.translatedText) return data.translatedText;
        throw new Error('LibreTranslate returned no text.');
      } catch (err) {
        console.warn('LibreTranslate failed, falling back to MyMemory:', err.message);
        // Fallback: MyMemory
        const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(truncateText(text, 5000))}&langpair=en|${targetLang}`;
        const response = await fetch(url);
        if (!response.ok) throw new Error(`MyMemory error: ${response.status}`);
        const data = await response.json();
        if (data.responseData && data.responseData.translatedText) {
          return data.responseData.translatedText;
        }
        throw new Error('Both translation services failed.');
      }
    }

    // ----- 4. FIX (LanguageTool) -----
    async function fixGrammar(text, language = 'en-US') {
      const url = 'https://api.languagetool.org/v2/check';
      const formData = new URLSearchParams();
      formData.append('text', truncateText(text, 5000));
      formData.append('language', language);

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      });

      if (!response.ok) throw new Error(`Grammar API error: ${response.status}`);

      const data = await response.json();
      if (!data.matches || data.matches.length === 0) return text;

      let corrected = text;
      const matches = data.matches.sort((a, b) => b.offset - a.offset);
      for (const match of matches) {
        if (match.replacements && match.replacements.length > 0) {
          const replacement = match.replacements[0].value;
          const before = corrected.substring(0, match.offset);
          const after = corrected.substring(match.offset + match.length);
          corrected = before + replacement + after;
        }
      }
      return corrected;
    }

    // ============================================================
    //  AI HELPERS
    // ============================================================
    function getSelectedText() {
      const sel = window.getSelection();
      if (sel.rangeCount && !sel.isCollapsed) {
        return sel.toString();
      }
      return null;
    }

    function getFullText() {
      return contentDiv.innerText;
    }

    function replaceSelectedText(newText) {
      const sel = window.getSelection();
      if (sel.rangeCount && !sel.isCollapsed) {
        const range = sel.getRangeAt(0);
        range.deleteContents();
        const textNode = document.createTextNode(newText);
        range.insertNode(textNode);
        range.setStartAfter(textNode);
        range.setEndAfter(textNode);
        sel.removeAllRanges();
        sel.addRange(range);
      } else {
        contentDiv.innerHTML = `<p>${newText.replace(/\n/g, '<br>')}</p>`;
        const range = document.createRange();
        range.selectNodeContents(contentDiv);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
      }
      contentDiv.focus();
      autoSave();
      updateWordCount();
    }

    function insertAtCursor(html) {
      const sel = window.getSelection();
      if (sel.rangeCount) {
        const range = sel.getRangeAt(0);
        const fragment = range.createContextualFragment(html);
        range.insertNode(fragment);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
      } else {
        contentDiv.innerHTML += html;
      }
      contentDiv.focus();
      autoSave();
      updateWordCount();
    }

    // ============================================================
    //  MAIN AI DISPATCHER (updated)
    // ============================================================
    async function performAI(action) {
      const selected = getSelectedText();
      const textToProcess = selected || getFullText();

      if (!textToProcess || textToProcess.trim().length === 0) {
        alert('No text to process. Please select some text or write something in the note.');
        return;
      }

      let result = '';
      let isReplace = true;

      loadingOverlay.classList.add('active');
      let dotCount = 0;
      const dotInterval = setInterval(() => {
        dotCount = (dotCount % 3) + 1;
        loadingStatus.innerHTML = `AI is thinking${'.'.repeat(dotCount)}`;
      }, 400);

      try {
        switch (action) {
          case 'summarize':
            result = await summarizeWithPuter(textToProcess);
            break;
          case 'generate': {
            const instruction = prompt('Describe what you want me to generate (e.g., "a list of 5 productivity tips"):', '');
            if (!instruction) {
              clearInterval(dotInterval);
              loadingOverlay.classList.remove('active');
              loadingStatus.innerHTML = 'AI is thinking...';
              return;
            }
            result = await generateWithDevToolBox(instruction);
            isReplace = false;
            break;
          }
          case 'translate': {
            const lang = await showLanguagePicker();
            if (!lang) {
              clearInterval(dotInterval);
              loadingOverlay.classList.remove('active');
              loadingStatus.innerHTML = 'AI is thinking...';
              return;
            }
            result = await translateText(textToProcess, lang);
            break;
          }
          case 'fix':
            result = await fixGrammar(textToProcess);
            break;
          default:
            return;
        }

        clearInterval(dotInterval);

        if (isReplace) {
          replaceSelectedText(result);
        } else {
          insertAtCursor(`<p>${result.replace(/\n/g, '<br>')}</p>`);
        }

        const msg = '✅ AI done!';
        saveStatus.textContent = msg;
        editorSaveStatus.textContent = msg;

      } catch (err) {
        clearInterval(dotInterval);
        let errorMsg = err.message || 'Unknown error';
        if (errorMsg.includes('429')) {
          errorMsg = 'Too many requests. Please wait a moment and try again.';
        } else if (errorMsg.includes('timeout')) {
          errorMsg = 'Request timed out. Please try again.';
        } else if (errorMsg.includes('HTML error')) {
          errorMsg = 'The AI service is temporarily unavailable. Please try again in a few seconds.';
        }
        alert(`AI Error: ${errorMsg}`);
        console.error('AI Error Details:', err);
      } finally {
        loadingOverlay.classList.remove('active');
        loadingStatus.innerHTML = 'AI is thinking...';
      }
    }

    // ============================================================
    //  AI BUTTONS
    // ============================================================
    $('ai-summarize').addEventListener('click', () => performAI('summarize'));
    $('ai-fix').addEventListener('click', () => performAI('fix'));
    $('ai-translate').addEventListener('click', () => performAI('translate'));
    $('ai-generate').addEventListener('click', () => performAI('generate'));

    // ============================================================
    //  INIT
    // ============================================================
    loadData();
    if (state.activeId) {
      showEditor(state.activeId);
    } else {
      showHome();
    }

    console.log('📝 Xiaomi Notes + AI (Puter.js + DevToolBox) ready!');
    console.log('🔧 Summarize: Puter.js (fallback: Pollinations)');
    console.log('✏️ Generate: DevToolBox AI (fallback: Pollinations)');
    console.log('🌍 Translate: LibreTranslate + MyMemory');
    console.log('🔧 Fix: LanguageTool');
  </script>
</body>
</html>
