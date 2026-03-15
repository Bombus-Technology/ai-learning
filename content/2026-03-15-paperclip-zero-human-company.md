---
title: "Paperclip — 零人公司的開源 AI Agent 協調系統"
url: "https://github.com/paperclipai/paperclip"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, 自動化, 系統設計, Multi-Agent]
category: "AI 應用"
draft: false
source_title: "Paperclip — Open-source orchestration for zero-human companies"
source_author: "Paperclip AI"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | Paperclip — Open-source orchestration for zero-human companies |
| 原文連結 | [https://github.com/paperclipai/paperclip](https://github.com/paperclipai/paperclip) |
| 作者 | Paperclip AI |
| 日期 | 2026-03-02 |

---

## 深度摘要

Paperclip 提出了一個大膽的定位：**如果 OpenClaw 是一個員工，Paperclip 就是一間公司**。它不是另一個 agent framework，也不是 chatbot 或 workflow builder——它是一個完整的「AI 公司營運系統」，提供組織架構圖、預算控管、治理機制、目標對齊，以及跨 agent 的協調與監督。你定義公司目標，雇用 AI 團隊（CEO、CTO、工程師、設計師、行銷），設定預算，然後按下啟動鍵——從一個 dashboard 監控所有 agent 的工作和成本。

> "Paperclip is a Node.js server and React UI that orchestrates a team of AI agents to run a business. Bring your own agents, assign goals, and track your agents' work and costs from one dashboard."

Paperclip 解決的核心問題非常具體：**你有 20 個 Claude Code 視窗同時開著，但搞不清楚誰在做什麼**。沒有 Paperclip，你手動蒐集散落各處的 context 提醒每個 bot、自己發明任務管理和溝通協調機制、忘記啟動定期任務、遇到迴圈失控浪費數百美元 token。有了 Paperclip，任務變成 ticket-based 對話串、context 從任務自動沿著專案和公司目標向上流動、agent 有月度預算限制、定期工作由 heartbeat 自動觸發、所有決策都有不可篡改的審計日誌。

> "Tasks are ticket-based, conversations are threaded, sessions persist across reboots. Context flows from the task up through the project and company goals — your agent always knows what to do and why."

技術上有幾個設計值得注意。**原子性執行**：任務 checkout 和預算扣除是原子操作，防止重複工作和失控花費。**持久化 agent 狀態**：agent 在 heartbeat 之間恢復同一任務的 context，不用從頭開始。**運行時技能注入**：agent 能在運行中學習工作流和專案 context，不需要重新訓練。**治理與回滾**：審批閘道強制執行，配置變更有版本控制，錯誤變更可以安全回滾。它支援 Bring Your Own Agent——只要能接收 heartbeat 就能被「雇用」。

> "Atomic execution. Task checkout and budget enforcement are atomic, so no double-work and no runaway spend."

最有前瞻性的是即將推出的 **Clipmart**——一個 agent 公司模板市集。你可以下載一整間預建的公司（完整組織架構、agent 配置、技能），一鍵匯入到你的 Paperclip 實例中。專案在兩週內獲得 23,000+ stars，說明市場對「multi-agent 企業級協調」的需求非常強烈——單一 agent 的能力已經夠好，瓶頸轉移到了如何協調多個 agent 一起工作。

> "If OpenClaw is an employee, Paperclip is the company."

---

## 原文引用

> "It looks like a task manager — but under the hood it has org charts, budgets, governance, goal alignment, and agent coordination."

> "Not a chatbot. Not an agent framework. Not a workflow builder. We tell you how to run a company made of them."

> "If it can receive a heartbeat, it's hired."

> "Agents bring their own prompts, models, and runtimes. Paperclip manages the organization they work in."

> "Goal-aware execution. Tasks carry full goal ancestry so agents consistently see the 'why,' not just a title."

---

## 討論紀錄

### Q1: 目前 Bombus 的 multi-agent 協調已經夠用，還是開始感受到 Paperclip 想解決的那種混亂？

**回答**: 目前尚未。

**延伸**: 目前的 agent 規模和 CLAUDE.md 規範還控制得住。不過隨著團隊人數增加或同時開發多個專案，這個痛點可能會浮現。值得留意的時機點是：當你發現自己開始「手動追蹤哪個 agent 在做哪件事」的時候。

### Q2: 在 Bombus 目前的 agent 設定中，agent 對「為什麼要做這件事」的 context 足夠嗎？

**回答**: 不太確認，之後可以詳細確認。

**延伸**: 這個可以之後實際檢視 CLAUDE.md 和各個 agent 的 prompt，看看是否有足夠的「why」context。Paperclip 的「目標祖先鏈」設計——每個任務帶著完整的目標脈絡，agent 不只知道「做什麼」還知道「為什麼」——會直接影響 agent 在需要自主判斷時的決策品質。

---

## 關鍵收穫

1. **Multi-Agent 的瓶頸從能力轉移到協調**：單一 agent 已經夠強，23,000+ stars 證明市場的痛點在「如何讓多個 agent 像一間公司一樣協作」。Bombus 目前規模尚可控，但值得持續關注——當手動追蹤成為負擔時就是引入協調系統的時機。
2. **目標對齊（Goal Alignment）是 agent 品質的隱性關鍵**：每個任務帶著完整的「為什麼」context，agent 在自主判斷時才不會偏離方向。這和 Harrison Chase 說的 context engineering 直接相關——Bombus 可以檢視目前的 agent prompt 是否包含足夠的「why」。
3. **治理機制是 multi-agent 系統的必要基礎設施**：預算控管（月度限額、原子性扣除）、審批閘道、審計日誌、配置回滾——這些在單一 agent 時不重要，但在多 agent 協作時是防止失控的基本防線。Bombus 在擴展 agent 使用時應優先建立這些機制。

---

> 想深入了解完整內容，請閱讀原文：[Paperclip](https://github.com/paperclipai/paperclip)
