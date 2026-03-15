---
title: "SBIR Skill — AI 驅動的政府補助申請工具與 Domain-Specific Skill 設計範例"
url: "https://github.com/backtrue/sbir-grants"
author: "Bombus Team"
date: 2026-03-15
tags: [AI Agent, MCP, 實務技巧, RAG]
category: "AI 應用"
draft: false
source_title: "SBIR Skill - AI 驅動的 SBIR 申請神器"
source_author: "BackTrue"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | SBIR Skill — AI 驅動的 SBIR 申請神器 |
| 原文連結 | [https://github.com/backtrue/sbir-grants](https://github.com/backtrue/sbir-grants) |
| 作者 | BackTrue |
| 日期 | 2026-01（持續更新至 2026-03） |

---

## 深度摘要

SBIR Skill 是一個極為完整的 AI 輔助工具，專為台灣中小企業申請 SBIR（小型企業創新研發計畫）政府補助而設計。這個專案的核心價值不在技術的花俏，而在**將一個原本需要 2-3 個月的痛苦流程，壓縮成 AI 引導的結構化工作流**。它整合了 84+ 個檔案、170,000+ 字的知識庫、122 個 FAQ、6 個完整方法論，並透過 MCP Server 讓 Claude 能直接搜尋、讀取、推薦內容。使用者只需回答 25 個結構化問題，AI 就能生成完整的 12-15 頁 Phase 1/Phase 2 計畫書。

> "設計目標：協助您更快、更完整地完成 SBIR 申請。加速撰寫流程，整合 84+ 個檔案的知識庫。"

技術架構上最值得學習的是它的**雙平台策略**。專案同時提供 MCP Skill（本機端 Claude Desktop 使用）和 SaaS 網頁版（Cloudflare Workers + D1 + R2 + Vectorize），兩者共享同一套知識核心（`shared_domain/` JSON 設定檔），確保輸出品質完全一致。更精緻的是它的「逆向移植（Reverse Porting）」架構——先在 MCP Skill 端開發高階 AI 演算法，驗證後再移植到 Web SaaS 平台，而非傳統的先 Web 後本機。

> "所有核心商業計算已全數抽離為 shared_domain/ JSON 設定檔，SaaS 與 MCP Server 同步掛載，輸出品質完全一致！"

在 AI 品質控管上，SBIR Skill 做了幾個值得注意的設計。**強制防幻覺機制**：將使用者的初訪調查表綁定為「絕對事實依據（Ground Truth）」，AI 生成內容必須以此為基準。**審查機制**：實作了類似 Word 追蹤修訂的功能，使用者可以對 LLM 的每一句編修選擇接受或拒絕。**6 維度即時診斷雷達**：用純規則式引擎（非 LLM）提供極速客觀評分。這些設計完美體現了「AI 加速執行，人類控管品質」的原則。

> "不要再盲目接受 AI 結果了！我們實作了如同 Word 的審查機制，您可以對 LLM 每一句的編修選擇接受或拒絕。"

搜尋引擎採用**混合式 RAG**：關鍵字搜尋 + 語意搜尋 + Cross-Encoder 重排序 + MMR 多樣性排序 + LRU 快取 + 同義詞擴展 + 時效加權。市場數據部分結合了 Tavily API 即時爬取研報、經濟部統計處 API、以及本地產業數據 JSON。這整套工具是「domain-specific AI skill」的教科書級範例——不是做一個通用的 AI 助手，而是把**特定領域的所有知識、流程、檢核標準都結構化後餵給 AI**。

> "混合式 RAG 與即時聯網：突破 AI 記憶瓶頸，市場規模已能自動呼叫 Tavily API 即時爬取研報，並結合 MMR 演算法與 Qwen 重排序過濾水分！"

---

## 原文引用

> "傳統方式的痛點：耗時 2-3 個月撰寫計畫書、到處找資料不知道從何開始、格式不確定擔心遺漏重點、成功率低投入大量時間卻失敗。"

> "強制防幻覺與過件守門員：直接將您的初訪調查表綁定為絕對事實依據 (Ground Truth)，並掛載地方型 SBIR 過件關鍵指南。"

> "6 維度即時診斷雷達：不再需要浪費時間等待 LLM 緩慢評估，全新純規則式引擎提供極速客觀雷達圖，一眼看穿專案弱點！"

> "單筆追蹤修訂 (AI Draft Auto-Edit)：不要再盲目接受 AI 結果了！我們實作了如同 Word 的審查機制。"

---

## 討論紀錄

### Q1: 有沒有可能把 Sencefore 的開發知識包成類似的 Skill？SBIR 補助功能能否結合到 SaaS 系統中？

**回答**: 有可能的，並且想要讓這個 skills 串接在系統中。SaaS 系統有一塊是在申請獎項，補助也可以結合在裡面。

**延伸**: Sencefore L6 文化影響力模組已有 L6.3 報獎檔案管理和預建獎項資料庫（100+ 台灣獎項），把 SBIR 這類政府補助也納入，就形成「獎項 + 補助」一站式申請平台——企業在 Sencefore 裡管理員工、做績效、跑專案，系統自動推薦適合申請的獎項和補助，再用 AI Skill 輔助生成申請文件。這是很強的產品差異化。

### Q2: 如果要做獎項+補助的 AI 功能，會選擇先在 Skill 端做 MVP，還是直接在 SaaS 開發？

**回答**: 在 Claude Code Skill 端做 MVP 驗證。

**延伸**: 這和 SBIR Skill 的路線一致——先在 Skill 端快速迭代演算法和知識結構，驗證 AI 輸出品質後再移植到 SaaS。成本低、迭代快，而且 Skill 本身在驗證期間就能直接給團隊使用。

---

## 關鍵收穫

1. **Domain-Specific Skill 是 AI 落地的最高效模式**：不是做通用 AI 助手，而是把特定領域的所有知識（84 個檔案、122 FAQ、6 個方法論）結構化後餵給 AI。SBIR Skill 證明了這種方式能將 2-3 個月的流程壓縮到幾十分鐘。Bombus 可以用同樣方法，將 Sencefore 的開發知識和獎項/補助申請知識各包成專屬 Skill。
2. **「逆向移植」是聰明的產品開發策略**：先在 MCP Skill 端驗證 AI 演算法和知識結構（成本低、迭代快），確認有效後再移植到 SaaS 平台。這比直接在 SaaS 上開發風險低得多，且 Skill 在驗證期間就能直接使用。
3. **防幻覺 + 追蹤修訂 + 規則式雷達 = AI 品質三道防線**：Ground Truth 綁定防止 AI 瞎編、Word 式審查機制讓人類逐句把關、純規則式引擎提供不依賴 LLM 的客觀評分。這三層設計可以直接參考到 Bombus 任何 AI 生成內容的品質控管中。

---

> 想深入了解完整內容，請閱讀原文：[SBIR Skill](https://github.com/backtrue/sbir-grants)
