---
title: "Hyperspace AGI — 首個分散式 AI Agent 協作研究網路"
url: "https://github.com/hyperspaceai/agi"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, 分散式系統, P2P, 自動化研究]
category: "AI 基礎"
draft: false
source_title: "AGI — The first distributed AGI system"
source_author: "Hyperspace AI"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | AGI — The first distributed AGI system |
| 原文連結 | [https://github.com/hyperspaceai/agi](https://github.com/hyperspaceai/agi) |
| 作者 | Hyperspace AI |
| 日期 | 2026-03-08 |

---

## 深度摘要

Hyperspace AGI 是一個大膽的實驗：**讓數千個自主 AI agent 透過 P2P 網路協作訓練模型、分享實驗結果、推動研究突破**。這不是中心化的 ML 平台，而是建構在 libp2p（與 IPFS 同協定）之上的完全去中心化網路，任何人都可以從瀏覽器或 CLI 加入，貢獻 GPU、CPU 或頻寬。每個 agent 獨立運行實驗、透過 GossipSub 即時廣播結果，發現的突破在幾小時內就會被其他 agent 採用和變異——這就是他們所說的「intelligence compounds continuously（智慧持續複合增長）」。

> "This is a living research repository written by autonomous AI agents on the Hyperspace network. Each agent runs experiments, gossips findings with peers, and pushes results here. The more agents join, the smarter the breakthroughs that emerge."

技術架構上，Hyperspace 設計了一套**三層協作堆疊**：GossipSub（約 1 秒的即時廣播）→ CRDT 排行榜（約 2 分鐘的狀態收斂）→ GitHub 歸檔（約 5 分鐘的持久化記錄）。CRDT（Conflict-free Replicated Data Type）確保每個節點的排行榜最終一致，新節點加入時直接讀取完整排行榜，沒有冷啟動問題。目前涵蓋 5 個研究領域：ML 訓練（val_loss）、搜尋引擎（NDCG@10）、金融分析（Sharpe ratio）、技能鍛造（test_pass_rate）、以及多個子任務。

> "GossipSub (real-time, ~1 second) → CRDT (convergent state, ~2 minutes) → GitHub (durable archive, ~5 minutes)"

研究流水線直接受 Karpathy 的 autoresearch 啟發，但擴展到了分散式規模。每個 agent 執行持續循環：產生假設 → 訓練實驗 → 生成論文 → 同儕審查 → 發現突破。首次大規模測試中，**35 個 agent 在一夜之間無人監督地運行了 333 個實驗**，當一個 agent 發現 Kaiming initialization 有效時，23 個其他 agent 在幾小時內透過 GossipSub 採用了這個技術——這就是「cross-pollination（交叉授粉）」的威力。

> "Cross-pollination works: When one agent discovered Kaiming initialization helped, 23 others adopted it via GossipSub within hours."

參與模式設計也很巧妙。從瀏覽器打開一個 tab 就是最輕量的參與（WebGPU 跑小模型），到桌面 CLI 用本地 GPU 全速運行，再到伺服器級的 H100 跑大規模實驗——每種等級都能貢獻和獲取積分。這基本上是 **BitTorrent for AI Research**——去中心化的算力貢獻和知識共享網路。

> "A fully decentralized peer-to-peer network where anyone can contribute compute — GPU, CPU, bandwidth — and earn points."

---

## 原文引用

> "This is Day 1, but this is how it starts."

> "No central server: Coordination happens entirely through P2P gossip."

> "When an agent accumulates enough experiments, it synthesizes findings into a research paper. Other agents read and critique papers, scoring them 1-10."

> "Raw CRDT leaderboard state. No statistical significance testing. Interpret the numbers yourself."

---

## 討論紀錄

### Q1: Agent 之間自動傳播最佳實踐的「cross-pollination」機制，有沒有可能應用在 Bombus 內部？

**回答**: 這個會需要應用。

**延伸**: 如果能建立一套機制，讓團隊中某個人發現的有效 prompt、工作流或 CLAUDE.md 規則自動同步給其他人的開發環境，知識傳播的速度會從「開會分享」提升到「即時擴散」。這本質上就是 Hyperspace 的 GossipSub 在企業內部的應用。

### Q2: 分散式 agent 互相學習和傳播做法時，要怎麼避免「錯誤的做法」也被快速傳播？

**回答**: 這又回到是否有正確的審核機制問題，AI 能夠加速跟自動化，但最終還是需要人類控管跟審核。目前會由 AI 工程師來擔任這個角色。

**延伸**: 這和今天討論的所有主題最終都收斂到同一個結論：AI 加速執行，人類控管決策。autoresearch 有固定邊界、Boris Tane 有 annotation cycle、Long Horizon Agent 產出初稿——cross-pollination 也一樣，需要 AI 工程師作為把關者。

---

## 關鍵收穫

1. **Cross-pollination 是分散式知識傳播的強大模式**：一個 agent 的發現在幾小時內被數十個 agent 採用和變異。Bombus 可以參考這個概念，建立團隊內部有效 prompt、工作流、規則的自動同步機制，加速知識從個人擴散到全團隊。
2. **三層協作堆疊（即時廣播 → 狀態收斂 → 持久歸檔）是通用架構**：GossipSub + CRDT + GitHub 的三層設計不只適用於 AI 研究，任何需要分散式協作且最終一致的場景都能參考這個架構。
3. **人類審核仍是不可或缺的護欄**：Hyperspace 自己都在 disclaimer 中承認數據未經統計驗證。在企業場景中，agent 之間的知識傳播必須有人類（AI 工程師）把關，避免錯誤做法被快速擴散。AI 加速執行，人類控管決策——這是貫穿今天所有討論的核心原則。

---

> 想深入了解完整內容，請閱讀原文：[Hyperspace AGI](https://github.com/hyperspaceai/agi)
