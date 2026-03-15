---
title: "進階 Prompt Engineering 技巧"
url: "https://example.com/prompt-engineering"
author: "Kevin"
date: 2026-03-13
tags: [Prompt Engineering, LLM, 實務技巧]
category: "AI 應用"
source_title: "Advanced Prompt Engineering Techniques"
source_author: "Anthropic Research"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | Advanced Prompt Engineering Techniques |
| 原文連結 | [https://example.com/prompt-engineering](https://example.com/prompt-engineering) |
| 作者 | Anthropic Research |
| 日期 | 2026-03-05 |

---

## 深度摘要

Prompt engineering 不僅僅是「寫好的指令」，它是一門關於如何有效地與 LLM 溝通的系統性方法論。本文從 Anthropic 的研究實務出發，整理了幾個在實際應用中效果最好的進階技巧。

> "Effective prompt engineering is not about tricks or hacks — it's about clearly communicating your intent, providing relevant context, and structuring the interaction for optimal results."

**Chain-of-Thought（思維鏈）** 是最廣為人知的技巧之一，但很多人忽略了一個關鍵細節：不是所有任務都需要 CoT。對於簡單的分類、提取、翻譯等任務，直接要求答案往往更快更準確。CoT 最適合需要推理、計算或多步驟判斷的任務。過度使用 CoT 反而可能引入不必要的推理錯誤。

> "Chain-of-thought prompting improves performance on tasks requiring multi-step reasoning, but can actually degrade performance on simple extraction tasks by introducing unnecessary reasoning steps."

**Few-shot vs Zero-shot** 的選擇也是一個常見的決策點。研究顯示，高品質的 few-shot 範例比大量低品質範例更有效。三到五個精心挑選的範例通常就足夠了，關鍵是範例要涵蓋邊界案例（edge cases），而不只是典型案例。

結構化輸出的 prompt 設計也有講究。使用 XML 標籤或 JSON schema 來定義輸出格式，比用自然語言描述更可靠。Anthropic 的模型特別擅長遵循 XML 標籤的指示，這也是 Claude 的 system prompt 大量使用 XML 的原因。

---

## 討論紀錄

### Q1: 在我們的 AI 引擎中，有哪些地方可以應用這些技巧？

**回答**: 最直接的應用是在 L2 的職能分析和 JD 生成。目前我們的 prompt 比較簡單，可以考慮加入 few-shot 範例來提升生成品質。另外，L5 的績效評估摘要也可以用 CoT 來讓推理過程更透明。

**延伸**: 好主意。建議先在 L2 的 JD 生成做 A/B 測試，用 3 個高品質的 JD 範例作為 few-shot input。

### Q2: XML 標籤 vs JSON schema，在實際使用中有什麼差異？

**回答**: 從我的經驗來看，XML 標籤在「自由形式+結構化」的混合輸出中更靈活，比如一段分析文字加上結構化的評分。JSON 則在純結構化資料輸出時更可靠，因為可以做 schema validation。

---

## 關鍵收穫

1. **CoT 不是萬能的**：簡單任務不需要思維鏈，過度使用反而有害。
2. **Few-shot 品質重於數量**：3-5 個涵蓋邊界案例的高品質範例最有效。
3. **結構化輸出用 XML/JSON**：比自然語言描述更可靠，XML 適合混合輸出，JSON 適合純結構化資料。

---

> 想深入了解完整內容，請閱讀原文：[Advanced Prompt Engineering Techniques](https://example.com/prompt-engineering)
