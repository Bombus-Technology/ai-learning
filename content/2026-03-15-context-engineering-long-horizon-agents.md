---
title: "Context Engineering 與 Long Horizon Agent — LangChain Harrison Chase 深度對談"
url: "https://www.youtube.com/watch?v=vtugjs2chdA"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, Context Engineering, LangChain, Agent Harness]
category: "AI 應用"
draft: false
source_title: "Context Engineering Our Way to Long-Horizon Agents: LangChain's Harrison Chase"
source_author: "Sequoia Capital (Training Data)"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | Context Engineering Our Way to Long-Horizon Agents |
| 原文連結 | [https://www.youtube.com/watch?v=vtugjs2chdA](https://www.youtube.com/watch?v=vtugjs2chdA) |
| 來賓 | Harrison Chase（LangChain 創辦人兼 CEO） |
| 頻道 | Sequoia Capital — Training Data 節目 |

---

## 深度摘要

Harrison Chase 在這場對談中提出了一個核心觀點：**所有關於 Agent 的工程，本質上都是 Context Engineering（脈絡工程）**。他認為「context engineering」這個詞精確地描述了 LangChain 過去所做的一切。無論是 compaction（壓縮）、sub-agent、skills、MCP，還是記憶系統，它們的本質都是在控制「什麼資訊進入 LLM 的 context」。在單次 LLM 呼叫中，你知道 prompt 是什麼、context 有什麼；但在 agent 中，第 14 步的 context 取決於前面 13 步的任意操作，這讓 trace 變得比傳統軟體的日誌重要得多。

> "Context engineering is such a good term. I wish I came up with that term. It actually really describes everything we've done at LangChain without knowing that that term existed."

Chase 將 agent 基礎架構的演進分為三個時代。第一個時代是原始的 text-in-text-out 模型，沒有 tool calling，只能做簡單的 chain。第二個時代是模型開始支援 tool calling，但還不夠好，需要用自訂的認知架構（cognitive architecture）做大量 scaffolding。第三個時代——也就是現在——是 **LLM 在迴圈中運行，自主決定如何操控 context 的時代**。這個演變催生了從 framework（框架）到 harness（控制裝置）的轉變。

> "We basically saw them using the same core algorithm but making improvements on context engineering. That's when we started working on deep agents."

關於 harness 工程的關鍵要素，Chase 指出幾個核心領域：理解模型訓練時使用的工具（Anthropic 訓練了檔案編輯工具，OpenAI 重度訓練 Bash）；compaction 策略；以及 sub-agent 之間的溝通設計。他特別強調，**做得最好的 harness 工程公司目前都在 coding 領域**——Claude Code 的成功很大程度歸功於 harness 本身，而不僅是模型。

> "I would argue a big reason for the popularity of Claude Code is the harness itself."

Chase 提出了建構 agent 和建構軟體的根本差異：軟體的邏輯全在程式碼中，但 agent 的邏輯一部分在程式碼，一部分在模型的黑箱中。這意味著 trace 取代原始碼成為理解系統的核心工件，測試需要融入人類判斷（LLM-as-judge），開發過程遠比傳統軟體更迭代。他也提到 **memory（記憶）** 是下一個大方向——讓 agent 能從 trace 中學習並自動更新自己的指令。

> "The source of truth for software is in code. For agents, it's a combination of code and traces."

---

## 社群重點整理

LangChain 創辦人 Harrison Chase 上了 Training Data podcast，深入聊了 Long Horizon Agent 為什麼現在才真正可用。所謂 Long Horizon Agent，就是能長時間自主運行、處理複雜多步驟任務的 AI Agent——不是問一句答一句，而是丟一個任務給它，它自己規劃、呼叫工具、可能跑幾十甚至上百步才完成。

### Long Horizon Agent 終於可以用了

模型變強（尤其 reasoning model），加上有效的 harness 設計（壓縮、規劃、檔案系統工具），兩邊共同演化才走到今天。Harrison 說回到兩年前，不會有人預測「檔案系統是 harness 的核心」——因為當時模型還沒被大量訓練在檔案操作上。

### 殺手級應用：都是「初稿」型任務

Agent 還做不到 99.99% 可靠度，但能跑很久做大量前期工作，人再來審查修改。判斷標準很簡單：這個任務的產出可以是初稿嗎？有人會審查嗎？都是「是」就很適合。

具體例子：

- **寫程式**：產出 PR，不是直接 push 到正式環境
- **AI SRE**：挖 log、跑分析、產出報告再交給人
- **研究報告**：金融研究、deep research，先出初稿再編輯
- **客服升級**：背景跑 Agent 整理完整事件報告，交接給真人客服

### Harness vs Framework vs Model 三層定義

- **Model**：LLM 本身，token 進 token 出
- **Framework**（如 LangChain）：提供抽象層，方便切換模型、整合工具，但對「怎麼用」不太有主見
- **Harness**（如 Deep Agents）：有主見的完整方案，內建規劃工具、壓縮策略、檔案系統存取

Harrison 預測：長期來看大多數公司不會自己建 harness，因為比建 framework 更難。大家會用現成的 harness，在 prompt/instruction 和工具層做差異化。

### 什麼讓 Harness 跑得好？

- **配合模型訓練的工具**：Anthropic 訓練了檔案編輯工具，OpenAI 重度訓練 Bash，要順著模型強項設計
- **壓縮策略**：長時間運行 context window 一定會滿，怎麼壓縮是大學問
- **子 Agent 協作設計**：常見失敗是子 Agent 回覆「看看我上面做的東西」但主 Agent 根本看不到
- **Prompt 品質**：這些 harness 的 system prompt 動輒好幾百行，品質差異直接反映在效能上

### Agent 開發的三個時代

- **第一代**：文字進文字出，GPT-3 時代，沒有 tool calling
- **第二代**：客製化認知架構，模型支援 tool calling 但推理不夠強，靠鷹架程式碼引導
- **第三代**：LLM 在迴圈中跑 + Context Engineering，2025 年中開始，差異化全在 context engineering 上

### 每個 Agent 都需要檔案系統

Harrison 堅信不管做什麼類型的 Long Horizon Agent，都該給它存取檔案系統的能力。壓縮時可以把訊息寫進檔案、大型 tool call 結果不用全塞進 context。他也區分了「真的檔案系統」和「虛擬檔案系統」——虛擬的可以做 context management，但沒辦法跑程式。

### 建 Agent 跟建軟體的根本差異

**差異一**：邏輯不全在程式碼裡。Agent 很大一部分邏輯來自模型這個非確定性黑盒子，必須實際跑它才知道行為。Trace 因此成為 Agent 開發的核心工件——傳統軟體裡 trace 是出問題才看，Agent 開發從第一天就盯著看。

**差異二**：迭代性質不同。Agent 出貨前不完全知道它會做什麼，開發者改的不是 code 是 system prompt，頻率遠高於傳統軟體。線上測試比離線測試更重要。

### Memory：Agent 的護城河

Harrison 分享了親身經歷：他有個跑了兩年的 email agent，累積了大量記憶。搬到新平台時即使 prompt 和工具一模一樣，少了那些記憶用起來就明顯比較差。Memory 本質上也是 context engineering，只是時間跨度更長。下一步是「睡眠時運算（sleep time compute）」：Agent 每天晚上自動回顧當天所有 trace，更新自己的指令。

### Agent UI 的未來

Long Horizon Agent 跑很久，UI 需要支援非同步（看板式管理多個 Agent）和同步（即時 chat 互動）的自然切換。純非同步也許未來可行，但現在人還是需要經常介入修正。另外 Agent 操作的「狀態」要看得到——光看 chat 對話不夠，需要能看到它改了什麼。

整場對話 Harrison 反覆強調：**Agent 的核心演算法極其簡單——就是 LLM 跑在迴圈裡。所有差異化都在 context engineering 上。**

---

## 原文引用

> "Context engineering is such a good term. I wish I came up with that term. It actually really describes everything we've done at LangChain without knowing that that term existed."

> "I would argue a big reason for the popularity of Claude Code is the harness itself."

> "The source of truth for software is in code. For agents, it's a combination of code and traces."

> "I very very strongly believe that right now if you're building a long horizon agent, you need to give it access to a file system."

> "I want implementation to be boring. The creative work happened in the annotation cycles."

---

## 討論紀錄

### Q1: Long Horizon Agent 的殺手級應用都是「初稿型任務」，Bombus 日常業務中還有哪些任務符合這個定義？

**回答**: 我們在開發每個新系統都是這樣的做法。

**延伸**: Bombus 的開發流程本身就是 Long Horizon Agent 的最佳實踐——AI 產出研究報告、架構設計、程式碼初稿，人來審查和做判斷性決策。Sencefore 從 Discovery 到 SRS 到實作，每一階段都是「初稿型」模式。

### Q2: Chase 強調 trace 是 agent 開發的核心工件，團隊在 agent 開發的 trace 可見性上做得夠嗎？

**回答**: 這部分我們需要再加強。

**延伸**: 隨著團隊越來越依賴 agent 做開發，trace 的可見性會直接影響除錯效率和品質。LangSmith 或類似的 tracing 工具可以列入評估清單。

---

## 關鍵收穫

1. **一切都是 Context Engineering**：Agent 的核心演算法極其簡單（LLM 跑在迴圈裡），所有差異化都在 context engineering 上——compaction、sub-agent 溝通、memory、skills 全部都是在控制「什麼進入 context」。這個框架可以統一理解我們所有 agent 相關的工作。
2. **Trace 是新時代的原始碼**：建構 agent 和建構軟體根本上不同，因為邏輯不全在 code 裡。Bombus 團隊需要加強 trace 可見性，這是 agent 品質的關鍵基礎設施。LangSmith 等工具值得評估。
3. **「初稿型任務」是最佳甜蜜點**：Agent 不需要 99.99% 可靠就能創造巨大價值，只要產出的是「初稿」而非最終結果。我們的開發流程已經是這個模式，可以更有意識地把這個框架推廣到更多業務場景。

---

> 想深入了解完整內容，請觀看原影片：[Context Engineering Our Way to Long-Horizon Agents](https://www.youtube.com/watch?v=vtugjs2chdA)
