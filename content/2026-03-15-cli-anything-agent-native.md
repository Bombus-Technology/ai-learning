---
title: "CLI-Anything — 讓所有軟體成為 Agent-Native"
url: "https://github.com/HKUDS/CLI-Anything"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, CLI, 自動化, Agent-Native]
category: "AI 應用"
draft: false
source_title: "CLI-Anything: Making ALL Software Agent-Native"
source_author: "HKUDS (香港大學數據科學實驗室)"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | CLI-Anything: Making ALL Software Agent-Native |
| 原文連結 | [https://github.com/HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) |
| 作者 | HKUDS（香港大學數據科學實驗室） |
| 日期 | 2026-03-08 |

---

## 深度摘要

CLI-Anything 的核心洞察是：**今天的軟體是為人類設計的，但明天的使用者將是 AI Agent**。目前 AI agent 擅長推理，但在操作真實的專業軟體時卻困難重重——現有方案不外乎脆弱的 UI 自動化（截圖+點擊）、有限的 API，或功能大幅縮水的重新實作。CLI-Anything 提出了一個根本性的解法：用一行指令，將任何有原始碼的軟體自動轉化為 agent 可以直接操控的 CLI 工具，不犧牲任何功能。

> "AI agents are great at reasoning but terrible at using real professional software. Current solutions are fragile UI automation, limited APIs, or dumbed-down reimplementations that miss 90% of functionality."

技術上，CLI-Anything 採用全自動化的 **7 階段流水線**：分析原始碼 → 設計命令架構 → 實作 Click CLI → 規劃測試 → 撰寫測試 → 文件化 → 發布。整個過程由 AI agent（Claude Code 或其他平台）自主完成，人類只需要指向目標軟體的路徑或 repo。產生的 CLI 具備 JSON 結構化輸出、有狀態的 REPL 互動模式、undo/redo 功能，並且直接呼叫真實軟體後端（例如 Blender 的 bpy、LibreOffice 的 headless mode）而非玩具替代品。

> "Authentic Software Integration — The CLI generates valid project files (ODF, MLT XML, SVG) and delegates to real applications for rendering. We build structured interfaces TO software, not replacements."

專案已經在 11 個複雜的專業軟體上驗證，涵蓋影像編輯（GIMP）、3D 建模（Blender）、音訊處理（Audacity）、辦公套件（LibreOffice）、直播（OBS Studio）、視訊剪輯（Kdenlive、Shotcut）等領域，累計 1,508 個測試全數通過。這不是概念驗證，而是生產級的工具——每個 CLI 都可以 pip install 後直接使用，agent 透過標準的 `--help` 和 `which` 命令就能發現和使用。

> "100% pass rate across all 1,508 tests — 1,073 unit tests + 435 end-to-end tests."

更深層的意義在於，CLI-Anything 定義了一個 **Agent-Native 軟體的標準方法論**（HARNESS.md）。這份 SOP 編碼了從 11 個專案中提煉出的實戰經驗：必須使用真實軟體渲染、注意 GUI 應用的「渲染差距」（效果在渲染時才套用）、濾鏡參數空間的差異、非整數幀率的時間碼精度問題等。CLI 被定位為 AI agent 與軟體世界之間的「通用介面」——比 GUI 自動化更可靠，比 API 更通用，比重新實作更完整。

> "CLI is the universal interface for both humans and AI agents: Structured & Composable — Text commands match LLM format and chain for complex workflows. Self-Describing — --help flags provide automatic documentation agents can discover."

---

## 原文引用

> "Today's Software Serves Humans. Tomorrow's Users will be Agents. CLI-Anything: Bridging the Gap Between AI Agents and the World's Software."

> "No screenshots, no clicking, no RPA fragility. Pure command-line reliability with structured interfaces."

> "The CLI MUST call the actual application for rendering. No Pillow replacements for GIMP, no custom renderers for Blender. Generate valid project files → invoke the real backend."

> "Requires strong foundation models — CLI-Anything relies on frontier-class models (e.g., Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.4) for reliable harness generation."

---

## 討論紀錄

### Q1: CLI-Anything「把既有軟體包成 CLI 讓 agent 操控」的思路，能否成為 Bombus 自然語言自動化工具的底層基礎設施？

**回答**: 這部分值得探討跟評估可行性。

**延伸**: 如果可行，架構可能是：員工用自然語言描述需求 → AI agent 理解意圖 → 透過 CLI-Anything 產生的 CLI 操控實際軟體。這等於把「自然語言 → 自動化」鏈路中最難的一環（與真實軟體對接）交給 CLI-Anything 解決。

### Q2: CLI-Anything 需要原始碼才能運作，企業閉源軟體怎麼處理？

**回答**: 可以考慮跟其他東西結合，例如 Bombus AI 的 Sage 平台，至少在開發的部分能有一些幫忙。

**延伸**: Sage 平台已有 AI 引擎基礎，CLI-Anything 可以幫 Sage 快速包裝內部開發工具（Git、CI/CD、測試框架、資料庫工具等有原始碼的部分），閉源軟體則走 API 或現有整合，兩條路並行。

### Q3: 如果要做最小可行驗證，會挑哪個工具或流程先試？

**回答**: 可能可以用自然語言自動化工具，因為很多東西可以連結 Python tools，大部分是寫檔放檔、Word、Excel 之類的工作。

**延伸**: Word/Excel/文件處理正好是 CLI-Anything 已驗證的領域（LibreOffice CLI 有 158 個測試全數通過）。用 Python 工具鏈（python-docx、openpyxl）加上 CLI-Anything 方法論，讓員工說「幫我把這份 Excel 的 A 欄資料整理成 Word 報告」就能自動完成，這個 MVP 很容易展示價值。

---

## 關鍵收穫

1. **CLI 是 Agent 與軟體之間的最佳介面**：比 GUI 自動化可靠（不依賴截圖和像素點擊）、比 API 更通用（任何有原始碼的軟體都可以）、比重新實作更完整（直接呼叫真實後端）。這個洞察對 Bombus 建構自然語言自動化工具有直接參考價值。
2. **7 階段流水線是可複製的方法論**：CLI-Anything 不只是一個工具，更是一套標準化的「軟體 Agent 化」SOP。Bombus 可以參考這套方法論，將內部開發工具逐步 Agent 化，整合到 Sage 平台中。
3. **文件處理是最佳 MVP 切入點**：Word/Excel 等日常行政庶務佔員工大量時間，且 Python 生態已有成熟工具鏈。從這裡開始驗證「自然語言 → 自動化」的價值，風險低、見效快。

---

> 想深入了解完整內容，請閱讀原文：[CLI-Anything](https://github.com/HKUDS/CLI-Anything)
