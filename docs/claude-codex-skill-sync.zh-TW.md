# 設計說明：一份 skill 資料夾，兩個 agent 共用

[English](claude-codex-skill-sync.md) | 繁體中文 | [简体中文](claude-codex-skill-sync.zh-CN.md)

這份說明記錄我怎麼讓同一套 skills 在 Claude Cowork 和 Codex 兩個 agent 裡都能用，而不用手動維護兩份。要使用這個 repo 的 skills 不需要看這份，它是我希望一開始就這樣做的做法。

最後更新：2026-11-26。

## 問題

我大部分討論用 Cowork，部分寫程式的工作用 Codex。很多 skills 兩邊都用得到。我從一開始就不想兩邊各放一份，因為每次修正都要改兩次。我希望一邊調整時，另一邊也能自動同步，所以在寫第一個 skill 之前，就先和兩邊的 AI 討論出一套做法。

這件事比複製檔案麻煩，有兩個原因：

- 兩個 agent 讀 skills 的地方不一樣。Codex 讀我電腦上的 skill 資料夾。Cowork 把 skills 存在我雲端的帳號裡，看不到我電腦上的檔案。
- 不是每個 skill 都要放兩邊。有些只在某一個專案裡才有意義。

## 想法

每個 skill 在我自己的電腦上只留一份正本。每個 agent 不是直接讀這份正本，就是從它取得副本。所有改動都從正本開始。

```
 正本：~/skills/<name>/SKILL.md          （我唯一會編輯的一份）
   |
   |-- Codex：   ~/.agents/skills/<name>  -> 指向正本的 symlink，改了立刻生效
   |
   '-- Cowork：  帳號層級的 skill         -> 每次改完要再提交一次
```

正本就是一般資料夾，一個 skill 一個資料夾，裡面放 `SKILL.md`。App 安裝時需要的 zip 檔只是備份，不當正本。

Claude Code 在這裡和 Codex 一樣。它讀本機資料夾裡的 skills（個人層級放在 `~/.claude/skills/<name>/SKILL.md`），也會跟著 symlink 讀到目標資料夾，所以不需要重新提交。

## 要設定的四個地方

1. **正本資料夾。** 一個 skill 一個資料夾，裡面放 `SKILL.md`。
2. **規範文件。** 放在你的筆記或知識庫裡，寫給 agent 照著做的文件。我把它叫作 agent wiki 頁。它的 `description` 寫「新增、修改、刪除 skill 之前先讀」，agent 就是靠這句找到它。範本在下面。
3. **兩個 agent 共用的偏好設定。** 讓每個新 session 一開始先看一遍規範文件和 skills。
4. **只給 Codex 的偏好設定。** 讓 Codex 把缺少的共用 skill 接起來。

這兩段偏好設定，是讓整套做法不用我每次開口要求的關鍵。Agent 要有東西告訴它規範文件存在，才會照著做。掃描只讀每份檔案的 `name` 和 `description`，成本很低。

### 兩個 agent 共用的偏好設定

```
每個新 session 的第一個輸入，先掃描兩個地方：規範文件資料夾和 skills 資料夾。
只讀每份檔案的 name 與 description，不讀全文。描述命中當下任務才讀全文。
判斷不出來是否命中時，先問我。
```

### 只給 Codex 的偏好設定

```
每個新 session 的第一個輸入，先掃描共用 skill 資料夾（<skills-master>），
和 Codex 自己的 skills 資料夾（<codex-skills-dir>）比對。缺的就建立指向正本的
symlink，已存在的不覆蓋。只回報新增或異常的項目。遵守當前的權限與審批機制；
無法寫入時，回報未完成的項目與原因。
```

`~/.agents/skills` 是目前 Codex 文件裡的使用者層級位置；舊版 Codex 用的是 `~/.codex/skills`。如果連結好的 skill 沒出現，請查你那個版本的文件。

### 規範文件

```
---
name: skill-sync-rules
description: 新增、修改、刪除 skill 之前先讀。說明正本放哪裡、各 agent 怎麼接到正本、
  改動怎麼記版本。
---

# Skill 同步規範

## 1. 先判斷是哪一種 skill
- 共用 skill：跨專案或跨 agent 使用。正本放在共用 skills 資料夾。需要同步，
  依第 2 到 4 節處理。
- 專案 skill：只有一個專案使用。正本放在該專案自己的 skills 資料夾。讀本機
  資料夾的 agent 直接從那裡讀。把 skills 存在雲端的 agent 仍然要提交一次。

## 2. 新增共用 skill
順序不能反：先建正本，再接各 agent。
1. 建立 <skills-master>/<name>/SKILL.md，含 version 與 updated 欄位，
   並建立 CHANGELOG.md，從 1.0 開始。
2. Codex：建立 <codex-skills-dir>/<name>，連到正本（symlink）。
3. Cowork：以新 skill 提交。

## 3. 修改共用 skill
1. 只改正本。升版本、更新日期，並在 CHANGELOG.md 加一行。
2. Codex：不用做任何事，連結已經指向正本。
3. Cowork：重新提交這次的改動。改完時提醒我：「這支 skill 的 Cowork 版需要
   重新提交」，否則 Cowork 會停在舊版。

## 4. 刪除共用 skill
1. 移除 Codex 的連結。
2. 從 Cowork 帳號移除這支 skill。
3. 刪除正本。

## 禁止
- 透過 Codex 的連結編輯，或直接編輯雲端那份。
- 另外手動維護共用 skill 清單。資料夾本身就是清單。
```

Cowork 在被要求提交 skill 時，會跳出一張審核卡片讓我同意。這就是第 3 節那個手動步驟。

## 每次改動都要記版本

沒有版本，就無法回答「哪一份是最新的」。每個 skill 都有：

- `SKILL.md` frontmatter 裡的 `version` 與 `updated` 欄位。版本號用 `major.minor`：小修正升小數（1.0 到 1.1），行為上的實質改變升整數（1.x 到 2.0）。不改變任何行為的錯字修正不需要升版。
- `SKILL.md` 旁邊的 `CHANGELOG.md`，最新版本放最上面：版本、日期、改了什麼、為什麼。通常一行就夠，大改動可以寫幾行。它不放在 `SKILL.md` 裡，agent 每次載入 skill 時就不用花 token 讀歷史。

有些 App 儲存 skill 時只保留名稱和說明，所以雲端那份可能不會留下 `version` 欄位。這也是為什麼要以正本和它的 changelog 為準，雲端那份拿來對照正本，而不是反過來。

## 專案指令也是同樣的做法

Agent 也會讀專案層級的指令檔，而且它們找的檔名不一樣：Claude Code 讀 `CLAUDE.md`，Codex 讀 `AGENTS.md`。我只留一份檔案，在專案資料夾裡把另一個名稱連到它：

```
ln -s CLAUDE.md AGENTS.md
```

這樣兩個 agent 讀到的就是同一份指令。需要不同行為的地方，檔案裡明確寫出來（例如「如果你是 Codex，用這個名稱」），而不是讓兩份檔案悄悄變得不一樣。

## 我遵守的規則

- 先建正本，再接各 agent。只存在雲端的 skill 沒有正本可以連，本機的 agent 會漏掉它。
- 只改正本。透過連結編輯雖然行得通，但很容易搞不清楚改的是哪個檔案。永遠不要直接編輯雲端那份：下次上傳會覆蓋它，它的改動也不會回到正本。（我曾經在雲端那份發現正本沒有的修正，只好手動搬回來。）
- 不另外維護共用 skill 清單。資料夾就是清單：掃描它、讀每個 `description`，永遠是最新的，手寫的清單會過期。
- 要刪除共用 skill：先刪連結，再從雲端帳號移除，最後刪正本。

## 這個做法沒有解決的事

- Cowork 仍然需要一個手動步驟。規範文件會讓 agent 提醒我，但提交我還是要自己同意。如果哪天有工具能把帳號層級的 skills 從本機資料夾同步出去，這會是第一個要自動化的地方。
- 每個 agent 不一樣的設定（路徑、名稱）還是要小心。這個 repo 的 skills 把這些值放在獨立的 `settings.md`，所以 `SKILL.md` 在每個地方都可以完全一樣。
