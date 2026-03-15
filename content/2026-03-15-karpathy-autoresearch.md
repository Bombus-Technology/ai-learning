---
title: "Karpathy 的 autoresearch — 讓 AI Agent 自主進行 LLM 研究"
url: "https://github.com/karpathy/autoresearch"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, LLM, 自動化研究, Karpathy]
category: "AI 應用"
draft: false
source_title: "autoresearch"
source_author: "Andrej Karpathy"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | autoresearch |
| 原文連結 | [https://github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch) |
| 作者 | Andrej Karpathy |
| 日期 | 2026-03-06 |

---

## 深度摘要

Karpathy 的 autoresearch 是一個極具前瞻性的實驗：**讓 AI Agent 自主進行 LLM 研究**。核心概念是將一個簡化的單 GPU LLM 訓練環境交給 AI agent，讓它在夜間自動進行實驗——修改程式碼、訓練 5 分鐘、檢查結果是否改善、保留或丟棄、重複循環。你早上醒來就能看到一整夜的實驗紀錄和（希望是）更好的模型。這不只是一個工具，更是對「AI 自主研究」這個概念的具體實踐。

> "The idea: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats."

架構設計上，整個 repo 刻意保持極簡——只有三個核心檔案。`prepare.py` 負責固定的資料準備和評估工具；`train.py` 是 agent 唯一會修改的檔案，包含完整的 GPT 模型、優化器和訓練迴圈；`program.md` 則是給 agent 的指令，類似一個輕量級的 skill。這個設計哲學非常有趣：**人類不再直接寫訓練程式碼，而是編寫「指導 AI 如何做研究」的 Markdown 文件**。這本質上是一種 meta-programming——你在編寫「研究組織的程式碼」，而非模型的程式碼。

> "The core idea is that you're not touching any of the Python files like you normally would as a researcher. Instead, you are programming the `program.md` Markdown files that provide context to the AI agents and set up your autonomous research org."

固定 5 分鐘時間預算的設計決策值得深思。每個實驗無論改了什麼（模型大小、batch size、架構），都嚴格在 5 分鐘內完成。這意味著每小時約 12 個實驗，一夜之間約 100 個實驗。這個設計讓不同實驗之間可以公平比較（用 val_bpb 作為統一指標），同時也意味著 autoresearch 會自動找到在你的硬體上最佳的 5 分鐘模型。代價是不同硬體平台之間的結果不可直接比較。

> "Training always runs for exactly 5 minutes, regardless of your specific platform. This means you can expect approx 12 experiments/hour and approx 100 experiments while you sleep."

Karpathy 在 README 開頭的「未來回顧」寓言特別引人注目——他描繪了一個 AI 完全取代人類做前沿研究的世界，而 autoresearch 就是這一切的起點。這個專案在發布不到兩週就獲得了 35,000+ stars，顯示社群對「AI 自主研究」這個方向有強烈共鳴。它也催生了多個平台 fork（MacOS、Windows），證明了這種範式的普適性。

> "Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies... This repo is the story of how it all began."

---

## 社群觀點

Andrej Karpathy 開源了 autoresearch 專案，能讓 AI agent 整夜自主進行 LLM 訓練實驗，人類只需早上起床看結果。

整個專案只有三個檔案：

- `prepare.py`：負責準備資料
- `train.py`：包含完整 GPT 模型與訓練迴圈
- `program.md`：人類撰寫的 agent 指令

工作流程很直覺：agent 修改程式碼 → 訓練 5 分鐘 → 檢查指標是否改善 → 保留或取消 → 重複。

每小時約跑 12 個實驗，只要睡一覺就有近百個結果等你檢視。

Karpathy 認為人類研究員的時代終將過去，未來的 AI 研究只需要搭配 Claude Code 等工具與一張 GPU 顯卡就能全面由 agent 全天候執行。

---

## 原文引用

> "One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of 'group meeting'. That era is long gone."

> "By design, training runs for a fixed 5-minute time budget (wall clock, excluding startup/compilation), regardless of the details of your compute. The metric is val_bpb (validation bits per byte) — lower is better."

> "Self-contained. No external dependencies beyond PyTorch and a few small packages. No distributed training, no complex configs. One GPU, one file, one metric."

---

## 討論紀錄

### Q1: autoresearch 的「不寫 code、寫 program.md」模式，在 Bombus 有沒有可以直接套用的場景？

**回答**: 希望藉由提升 Bombus 員工的 AI 職能，由 AI 部門開發一套讓員工只要用自然語言就能建立日常自動化流程的工具，取代過往複雜的 RPA 操作模式。希望員工也能學習如何用新技能打造比較簡單的智能化流程。

**延伸**: 這和 autoresearch 的 `program.md` 模式高度吻合——Karpathy 證明了一個 Markdown 文件就能定義 AI agent 的完整行為，Bombus 則是要讓每個員工都能寫出自己的「program.md」來驅動工作流自動化。

### Q2: 員工用自然語言建流程，任務邊界模糊，要怎麼設計「護欄」？

**回答**: 事先建立好每個系統跟功能的權責劃分，若有需要審核的就走審核流程，但主要降低日常行政庶務的負擔。

**延伸**: 很務實的做法——低風險的行政庶務直接執行，高風險的動作自動觸發審核。這就是 autoresearch 「固定邊界內自主實驗」精神在企業場景的延伸。

### Q3: 自然語言自動化工具會放在 Sencefore 平台內，還是獨立項目？

**回答**: 獨立的兩個項目。Sencefore 是給客戶的 SaaS 產品，自然語言自動化是 Bombus 內部的 AI 職能提升工具。兩個產品、兩條路線，互不干擾但可以共享技術經驗。

---

## 關鍵收穫

1. **Meta-programming 是新範式**：autoresearch 證明了「寫指令文件指導 AI」比「自己寫程式碼」更高效。這個思維可以直接應用到 Bombus 的內部自動化——讓員工用自然語言定義流程，AI agent 負責執行。
2. **固定邊界 + 自主實驗 = 安全的 AI 自動化**：Karpathy 用「5 分鐘 + 單一指標 + 單一檔案」劃定了安全邊界。企業場景同理——先定義好權責和審核規則，AI 在框架內自由運作。
3. **極簡架構的威力**：三個檔案、一張 GPU、一個指標。這種刻意的極簡設計讓 35,000+ 人能快速理解和參與。工具設計應該追求同樣的簡潔。

---

> 想深入了解完整內容，請閱讀原文：[autoresearch](https://github.com/karpathy/autoresearch)
