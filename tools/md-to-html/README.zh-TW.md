# md-to-html

[English](README.md) | 繁體中文 | [简体中文](README.zh-CN.md)

版本 1.0，最後更新 2026-11-18。

我習慣用 Markdown 寫筆記，常常是 AI agent 跟我一起改。但有些筆記在編輯器裡很難讀：十幾欄的比較表被擠到每格都在換行，長筆記也沒辦法把段落收起來。這個 skill 會把 `.md` 轉成一頁比較好讀的 HTML：寬表可以左右捲動，表頭和前兩欄固定不動；Obsidian 的 callout 變成可以收合的區塊；手機上看版面也會自動調整。

和 agent 一起用的關鍵是一條規則：`.md` 是唯一的來源。你看著網頁說「這段收起來」、「加一個跳到那個標題的連結」，agent 會去改 `.md`，再重新產生網頁，不會直接改 HTML，兩邊就不會對不上。

## 需求

- 一個能在你檔案所在的電腦上執行指令的 agent（例如 coding agent，或有終端機工具的桌面 app）。
- Python 3 和 `markdown` 套件，要裝在執行 script 的同一個 `python3` 底下，例如 `python3 -m pip install --user markdown`。Homebrew 管理的 Python 可能會拒絕，這時改用虛擬環境（venv）。也可以請 agent 幫你裝。

不需要任何帳號或 ID。沒有 `settings.md` 時，skill 用 `default` 主題，網頁語言設為英文。

## 設定

把整個 skill 資料夾（含 `scripts/` 和 `assets/`）複製到 agent 的 skills 目錄（位置依工具而定）。

選填：把 `settings.example.md` 在同一個資料夾複製成 `settings.md`，可以改兩個預設值：

- 預設主題：沒指定主題時用哪一個。可以是 `assets/themes/` 裡的檔名（不含 `.css`，例如 `dark`），或是你自己的 `.css` 檔路徑。
- 網頁語言：寫進網頁的語言代碼，例如 `zh-Hant`、`ja`。瀏覽器靠它挑字型，螢幕閱讀器靠它選語音。

## 用法

用你自己的話說就可以，例如「把 notes.md 轉成 HTML 給我看」。agent 會執行 script，告訴你 HTML 檔在哪裡，用瀏覽器打開就好。之後內容有改，重新整理分頁就看得到。

看著網頁時，也可以直接提要求：「Background 那段收起來」、「加一個跳到 Pricing 的連結」、「換成深色主題」。agent 會把這些寫進 `.md`。

## 主題

版面在 `assets/base.css`，顏色和字型放在 `assets/themes/` 底下的小檔案，這一版附 `default`（淺色）和 `dark`（深色）。想做自己的主題，把 `default.css` 在同一個資料夾複製成新檔名，改裡面的值，就能用那個名字指定，不用改 script。主題檔也可以加自己的 CSS 規則，會蓋過基本版面。

## 補充

- 所有東西都內嵌在 HTML 檔裡，離線也能打開，也能單獨傳給別人。
- 每次產生網頁都會覆蓋舊的 HTML。不要自己改 HTML，要改就改 `.md`。
- 支援的 Obsidian 語法：同一個檔案內的 `[[#標題]]`、`[[#標題|顯示文字]]` 連結，以及 callout（`> [!note]- 標題` 預設收起，`+` 或不加符號預設展開）。連到其他檔案的連結不會轉換。
- `.md` 開頭的 YAML frontmatter 不會出現在網頁上。
- 程式碼區塊或 `行內程式碼` 裡的 Obsidian 語法會照原樣顯示，所以解說語法的筆記也能正確呈現。
- callout 裡的標題沒有錨點，跳到這些標題的連結不會動。
- 每次執行都會寫 log 到 `/tmp/md_to_html.log`，出問題時 agent 可以自己看。

## 升級到新版本

換掉 skill 資料夾時，你的 `settings.md` 和自己加進 `assets/themes/` 的主題可能會一起被刪掉。升級前先複製到其他地方，升級完再搬回來。

如果新版需要新的設定，`CHANGELOG.md` 會寫明。

## 在雲端或手機上執行

這個 skill 要靠終端機執行 script，所以在沒有終端機的環境（例如大部分手機 app）不能用。如果環境有終端機、但只保存 `SKILL.md`，把 `settings.md` 的內容貼到 `SKILL.md` 最後面，標題用 `## Settings (pasted)`，`scripts/` 和 `assets/` 也要一起放進去。升級會換掉 `SKILL.md`，所以每次升級後都要重貼。

## 授權

MIT 授權，見 repo 根目錄的 [LICENSE](../../LICENSE)。
