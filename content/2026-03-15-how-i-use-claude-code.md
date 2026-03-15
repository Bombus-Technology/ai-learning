---
title: "How I Use Claude Code — Boris Tane 的 Claude Code 工作流"
url: "https://boristane.com/blog/how-i-use-claude-code/"
author: "Bombus Team"
date: 2026-03-15
tags: [Claude Code, AI Agent, 實務技巧, 工作流]
category: "工程實務"
draft: false
source_title: "How I Use Claude Code"
source_author: "Boris Tane"
---

## 原文資訊

| 項目 | 內容 |
|------|------|
| 標題 | How I Use Claude Code |
| 原文連結 | [https://boristane.com/blog/how-i-use-claude-code/](https://boristane.com/blog/how-i-use-claude-code/) |
| 作者 | Boris Tane（Cloudflare 工程主管，Baselime 前創辦人） |
| 日期 | 2026-02-10 |

---

## 深度摘要

Boris Tane 的核心原則只有一句話：**「在你審查並核准書面計畫之前，絕對不要讓 Claude 寫程式碼」**。作為 Cloudflare 的工程主管，他把與 Claude Code 的協作分成三個明確階段：研究（Research）、規劃（Planning）、實作（Implementation）。這個分離的關鍵在於——研究防止「無知的改動」，規劃防止「錯誤的改動」，而人類的判斷在最關鍵的決策點介入。

> "Never let Claude write code until you've reviewed and approved a written plan."

**研究階段**的重點是讓 Claude 深入分析相關程式碼，並將發現寫成 `research.md`。Tane 強調要用「deeply」、「in great details」、「intricacies」等語言引導，避免 Claude 只做表面掃描。這個持久化的 Markdown 文件讓他能在規劃開始前驗證 Claude 的理解是否正確。沒做研究就直接實作的常見失敗模式：函式忽略現有的快取層、migration 不遵守 ORM 慣例、邏輯在其他地方已經存在卻重複實作。

> "This persistent markdown artifact allows him to verify Claude's understanding before planning begins, preventing implementations that work in isolation but break surrounding systems."

**規劃階段**最精華的部分是「標註循環（Annotation Cycle）」。Claude 先產出 `plan.md` 草稿，Tane 接著直接在文件中加入行內標註——修正假設、否決方案、補充領域知識。這個循環重複 1-6 次，全程帶著「don't implement yet」的護欄。Markdown 文件在這裡扮演的角色是**人機之間的共享可變狀態**，讓逐項的決策能基於產品優先順序和工程取捨來做。

> "The markdown acts as shared mutable state, allowing item-level decisions based on product priorities and engineering trade-offs that Claude cannot independently determine."

**實作階段**反而是最簡潔的。Tane 用一個標準化的 prompt 啟動全部實作，過程中的回饋極度精簡。當方向完全錯誤時，他選擇完全 revert 並重新規劃，而不是打補丁式地修修補補。

> "Read deeply, write a plan, annotate the plan until it's right, then let Claude execute the whole thing without stopping, checking types along the way."

---

## 完整中文翻譯

以下為原文完整翻譯，適合非工程背景的讀者閱讀學習。

---

### 我如何使用 Claude Code

我使用 Claude Code 作為主要開發工具大約 9 個月了。我的工作流和一般的 AI 程式設計方式有根本性的不同。大多數開發者是打 prompt、然後對著錯誤反覆修正，或是組合各種工具和框架。我採用的是一套有紀律的方法論，圍繞著一個核心原則：**「在你審查並核准書面計畫之前，絕對不要讓 Claude 寫程式碼」**。

這和常見的做法形成對比，那些做法「在碰到任何非小事的任務時就完全崩潰」。我的方法強調規劃和執行的分離，維持開發者對架構決策的控制，並且用最少的 token 消耗產出更好的結果。

---

### 第一階段：研究

每個有意義的任務都從深度閱讀指令開始，要求 Claude 徹底理解相關程式碼段落。發現的內容必須寫成持久化的 Markdown 文件，而不是口頭摘要。

範例 prompt：

- 「深入閱讀這個資料夾，深入理解它的運作方式、功能和所有特性。完成後，把你的學習和發現寫成一份詳細報告，存為 research.md」
- 「詳細研究通知系統，理解它的細節和複雜之處，然後寫一份詳細的 research.md 文件」
- 「走過整個任務排程流程，深入理解它，並尋找潛在的 bug……寫一份詳細報告」

**用語非常重要。**「deeply」、「in great details」、「intricacies」這些詞是訊號，告訴 Claude 表面層次的閱讀是不夠的。沒有這些指令，Claude 可能只會粗略瀏覽內容。

這份書面產出有多重用途：

- 它提供一個可以審查驗證的表面
- 它讓你能在規劃開始前修正誤解
- 它防止因為基礎理解錯誤而導致的實作失敗

我認為這是「AI 輔助程式設計中最昂貴的失敗模式」——不是語法錯誤或糟糕的邏輯，而是那些**單獨來看能運作、卻會破壞周圍系統**的實作。例子包括：函式忽略現有的快取層、migration 沒有考慮 ORM 慣例、或是端點重複了已存在的邏輯。

---

### 第二階段：規劃

審查完研究報告後，我會要求 Claude 在獨立的 Markdown 文件中撰寫詳細的實作計畫。

範例請求：

- 「我想建一個新功能 [描述]，擴展系統以達成 [成果]。寫一份詳細的 plan.md 文件，說明如何實作。包含程式碼片段」
- 「列表端點應該支援 cursor-based 分頁，而不是 offset。寫一份詳細的 plan.md 說明如何實現」

產生的計畫包含詳細的解釋、展示實際改動的程式碼片段、要修改的檔案路徑，以及關於取捨的考量。

我使用自訂的 Markdown 文件，而不是 Claude Code 內建的 plan mode。我覺得內建的 plan mode 很爛（sucks），我更喜歡對專案中的持久化產出物有完全的控制。

一個一致的技巧是，在要求計畫時附上開源專案的參考實作：「這是他們做 sortable ID 的方式，寫一份 plan.md 解釋我們如何採用類似方法。」**Claude 在有具體參考實作時表現會顯著提升**，遠好於從零設計。

---

### 標註循環（Annotation Cycle）

這是我工作流中最獨特、最有價值的部分——也是我貢獻最大價值的階段。

流程如下：

1. Claude 撰寫 plan.md
2. 我在編輯器中審查
3. 我在文件中直接加入行內標註
4. 我把 Claude 送回去：「我在文件中加了一些備註，處理所有備註並更新文件。先不要實作（don't implement yet）」
5. Claude 更新計畫
6. 循環重複 1-6 次，直到我滿意

行內標註的範圍和風格多樣：

- **領域知識**：「用 drizzle:generate 做 migration，不要用 raw SQL」
- **修正假設**：「不對——這應該是 PATCH，不是 PUT」
- **否決方案**：「整個區塊刪掉，這裡不需要快取」
- **解釋脈絡**：「queue consumer 已經處理重試了，所以這個重試邏輯是多餘的」
- **重組區塊**：「visibility 欄位應該在列表本身上，不是在個別項目上……相應地重新調整 schema 區塊」

明確的**「先不要實作」護欄**非常關鍵，因為 Claude 否則會過早跳進寫程式碼的階段。

#### 為什麼這個方法有效

Markdown 文件在開發者和 Claude 之間建立了**「共享可變狀態」**。我可以用自己的節奏思考，在問題存在的精確位置做標註，並且在不失去脈絡的情況下重新投入。這和透過聊天訊息來引導有根本性的不同——在聊天中，要回顧之前的決策需要一直往回捲。

三輪標註就能把一個通用的計畫轉變成一個完美契合現有系統的計畫。Claude 擅長理解程式碼、提出解決方案、撰寫實作，但它缺乏關於**產品優先順序、使用者痛點和工程取捨**的知識。標註循環就是注入這些人類判斷的過程。

#### 待辦清單

在實作之前，我會要求一個細粒度的任務拆解：「在計畫中加入一個詳細的待辦清單，包含完成計畫所需的所有階段和個別任務——先不要實作」

這個檢查清單在實作期間作為進度追蹤器，Claude 會在完成時逐項標記。這在持續數小時的 session 中特別有價值，因為進度的可見性很重要。

---

### 第三階段：實作

當計畫獲得批准，我使用一個標準化的實作指令：

「實作全部。當你完成一個任務或階段時，在計畫文件中標記為完成。在所有任務和階段都完成之前不要停下來。不要加入不必要的註解或 jsdoc，不要使用 any 或 unknown 類型。持續執行 typecheck 確保你沒有引入新問題。」

每個部分都編碼了特定意圖：

- **「實作全部」**——完成所有計畫中的項目，不要挑選
- **「在計畫文件中標記為完成」**——計畫是進度的唯一真實來源
- **「在所有任務和階段都完成之前不要停下來」**——保持動量，不要中斷
- **「不要加入不必要的註解或 jsdoc」**——保持程式碼乾淨
- **「不要使用 any 或 unknown 類型」**——維持嚴格的型別紀律
- **「持續執行 typecheck」**——及早發現問題，而不是到最後才發現

我幾乎在每個實作 session 中都用這個完全相同的措辭（只有微小的變化）。到這個階段，每個決策都已經做出並驗證了。**「我希望實作是無聊的。創造性的工作發生在標註循環中。一旦計畫正確，執行應該是直截了當的。」**

規劃階段防止了 Claude 在早期做出錯誤假設並層層疊加的問題。沒有規劃的話，「Claude 在早期做了一個合理但錯誤的假設，在上面建構了 15 分鐘，然後我必須拆解一連串的改動。」

---

### 實作期間的回饋

在執行期間，我的角色從架構師轉為監督者。我的 prompt 變得顯著更短。

需要修正時，訊息變得極簡：

- 「你沒有實作 `deduplicateByTitle` 函式。」
- 「你把設定頁面建在主應用裡，應該在管理後台，移過去。」

Claude 已經從計畫和持續的 session 中擁有完整脈絡，簡短的修正就足夠了。

前端工作產生最多的迭代回饋：

- 「wider（更寬）」
- 「still cropped（還是被裁切了）」
- 「there's a 2px gap（有 2px 的間距）」

有時候截圖會伴隨視覺問題的回報，比描述更快地傳達問題。

現有程式碼作為持續的參考點：「這個表格應該和 users 表格看起來完全一樣，相同的標題、相同的分頁、相同的列密度。」這比從零設計更精確，因為成熟的程式碼庫包含現有的模式範例。Claude 通常會在做修正前先閱讀被參考的檔案。

當方向錯誤時，我會 revert 而不是打補丁：「我 revert 了所有東西。現在我只想讓列表視圖更簡約——其他什麼都不要。」**在 revert 後縮窄範圍，通常比逐步修復錯誤方向產出更好的結果。**

---

### 保持在駕駛座上

雖然把執行委託給 Claude，我從不給予完全自主權。我透過 plan.md 的標註來引導絕大多數的方向。

這很重要，因為 Claude 可能會提出技術上正確但脈絡上錯誤的解決方案——過度工程的方案、改變了影響系統其他部分的公開 API 簽章、或在更簡單的替代方案存在時選擇不必要的複雜選項。我擁有更廣的系統脈絡、對產品方向的理解，以及 Claude 所缺乏的工程文化知識。

**從提案中挑選：** 當 Claude 識別出多個問題時，我逐一評估：「第一個，直接用 Promise.all……第三個，提取成獨立函式……忽略第四和第五個，不值得增加複雜度。」基於當前重要性做逐項決策。

**修剪範圍：** 非必要的功能會被主動砍掉：「從計畫中移除下載功能，我現在不想實作這個。」這防止了範圍蔓延。

**保護現有介面：** 硬性約束保護不該變動的東西：「這三個函式的簽章不能改，應該讓呼叫端適應，不是函式庫。」

**覆寫技術選擇：** 工作過程中會出現具體偏好：「用這個模型替代那個」或「用這個函式庫的內建方法，不要自己寫。」小決策用快速、直接的覆寫處理。

Claude 處理機械性的執行，我做判斷性的決策。計畫在前期捕捉了主要決策，選擇性的指導處理實作期間浮現的小決策。

---

### 單一長 Session

我在**單一長 session** 中執行研究、規劃和實作，而不是拆分成多個對話。一個 session 可能從深度閱讀開始，經過三輪計畫標註，然後在連續對話中執行完整實作。

我沒有遇過大家常討論的「消耗 50% context window 後效能下降」的問題。到實作階段時，Claude 已經花了整個 session 建立理解——在研究期間閱讀檔案、在標註循環中精煉心智模型、吸收領域知識的修正。

當 context 滿了，Claude 的自動壓縮（auto-compaction）會維持足夠的脈絡繼續工作。計畫文件作為持久化的產出物，在壓縮中以完整形式存活。我隨時可以參考它。

---

### 一句話總結這個工作流

**「深入閱讀，寫計畫，標註計畫直到它正確，然後讓 Claude 一路執行到底，過程中持續做型別檢查。」**

沒有魔法 prompt，沒有精巧的系統指令，沒有聰明的 hack。只是一個有紀律的流水線，將思考和打字分離。研究防止無知的改動。計畫防止錯誤的改動。標註循環注入人類判斷。實作指令實現不間斷的執行。

**「試試我的工作流，你會想著自己以前沒有一份標註過的計畫文件放在你和程式碼之間，到底是怎麼用 coding agent 交付任何東西的。」**

---

## 原文引用

> "Never let Claude write code until you've reviewed and approved a written plan."

> "Claude works dramatically better when it has a concrete reference implementation."

> "The markdown acts as shared mutable state, allowing item-level decisions based on product priorities and engineering trade-offs that Claude cannot independently determine."

> "I want implementation to be boring. The creative work happened in the annotation cycles. Once the plan is right, execution should be straightforward."

> "Try my workflow, you'll wonder how you ever shipped anything with coding agents without an annotated plan document sitting between you and the code."

---

## 討論紀錄

### Q1: Boris Tane 的研究→規劃→標註循環→實作方法，和我們目前團隊的做法差距在哪？

**回答**: 跟目前的做法非常相似，可以直接採用。

**延伸**: 代表 Bombus 團隊的工作流已經走在正確方向上。這篇文章可以直接作為團隊其他成員的入門教材，特別是非工程背景的同事。

### Q2: Tane 不用內建 plan mode 而用自己的 plan.md，和我們目前的 agent + rules 自動化相比如何？

**回答**: 對於不懂的人 plan mode 非常方便，但如果自己有時間跟能力，用 plan.md 會是更好的做法。

**延伸**: Plan mode 降低入門門檻，適合不熟悉的人快速上手；plan.md 給你完全的控制權。對 Bombus 來說，非工程背景的人先從 plan mode 開始，等熟練後自然過渡到 plan.md 模式，是很合理的學習路徑。

---

## 關鍵收穫

1. **「先不要實作」是最重要的護欄**：研究和規劃階段的紀律決定了最終品質。讓 Claude 在錯誤假設上建構 15 分鐘再拆解，遠比花 3 輪標註循環把計畫修正到位更浪費。
2. **Markdown 是人機協作的最佳介面**：`plan.md` 作為「共享可變狀態」，讓人類可以用自己的節奏思考、精確標註、反覆修正，比聊天式的來回更有效率。這篇文章可以直接作為 Bombus 非工程同仁學習 Claude Code 的入門教材。
3. **實作應該是無聊的**：所有創造性的工作（架構決策、範圍修剪、技術選型）都在標註循環中完成。實作階段只是機械性的執行，回饋精簡到一兩個字就夠了。

---

> 想深入了解完整內容，請閱讀原文：[How I Use Claude Code](https://boristane.com/blog/how-i-use-claude-code/)
