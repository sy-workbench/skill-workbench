#!/usr/bin/env python3
"""
md_to_html.py: turn one Markdown file into a styled, self-contained HTML preview.

# Input format
- argv[1]: path to a .md file.
- --out PATH (optional): where to write the HTML. Default: next to the .md, same name, .html.
- --theme NAME_OR_PATH (optional): a theme name from assets/themes/ (for example
  `default`, `dark`), or a path to your own .css file. Default: `default`.
- --lang CODE (optional): value of <html lang>. Default: `en`.

# Workflow
1. Read the .md and strip YAML frontmatter. Set code (fenced blocks and inline code) aside so the
   next step leaves it untouched.
2. Convert Obsidian-only syntax: [[#Heading]] / [[#Heading|label]] links and
   > [!type]- / > [!type]+ callouts (collapsed / expanded).
3. Convert the rest with python-markdown (tables, fenced code, toc, sane lists, nl2br).
4. Wrap tables in a horizontally scrollable box.
5. Inline base.css plus the theme's CSS and write one self-contained .html file.

### Edge Cases
- Input file missing: log an error and exit 1.
- Theme not found: log an error that lists the available themes and exit 1.
- Empty file: writes a page with an empty body.
- Extension is not .md: logs a warning and converts anyway.
- python-markdown not installed: log the install command and exit 1.
- Output folder missing or not writable, or the .md is not UTF-8: log the error and exit 1.
- Obsidian syntax inside code (fenced blocks or `inline code`) is shown as written, not converted.
- Headings inside a callout get no id, so a [[#...]] link to them does not jump.

# Output files
- The .html file (path printed on the last line of stdout).
- Log: /tmp/md_to_html.log, lines formatted `[YYYY-MM-DD HH:MM:SS] message`.

# Reference
- python-markdown: https://python-markdown.github.io/

# Dependencies
- Python 3, markdown (`pip install markdown`).
"""
import argparse
import datetime
import html as html_lib
import os
import re
import sys

LOG_PATH = "/tmp/md_to_html.log"
HERE = os.path.dirname(os.path.abspath(__file__))
THEME_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "themes"))
BASE_CSS = os.path.normpath(os.path.join(HERE, "..", "assets", "base.css"))


def log(msg):
    line = f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def available_themes():
    if not os.path.isdir(THEME_DIR):
        return []
    return sorted(os.path.splitext(n)[0] for n in os.listdir(THEME_DIR) if n.endswith(".css"))


def load_css(theme):
    """base.css + one theme. A theme is a name in assets/themes/ or a path to a .css file."""
    if theme.endswith(".css") or os.sep in theme:
        theme_path = os.path.expanduser(theme)
        if not os.path.isfile(theme_path) and os.sep not in theme:
            # "dark.css" with no folder: also try it as a theme name in assets/themes/.
            theme_path = os.path.join(THEME_DIR, theme)
    else:
        theme_path = os.path.join(THEME_DIR, theme + ".css")
    if not os.path.isfile(theme_path):
        raise FileNotFoundError(
            f"theme not found: {theme} (available: {', '.join(available_themes()) or 'none'})"
        )
    with open(BASE_CSS, encoding="utf-8") as f:
        base = f.read()
    with open(theme_path, encoding="utf-8") as f:
        theme_css = f.read()
    # The theme comes last, so it can override any base rule as well as set variables.
    return base + "\n/* ---- theme ---- */\n" + theme_css


WRAP_TABLE = re.compile(r"(<table>.*?</table>)", re.DOTALL)

# Obsidian heading links: [[#Heading]] or [[#Heading|label]] -> [label](#slug).
# The slug uses the same function as the toc extension, so links and heading ids match.
WIKILINK_RE = re.compile(r"\[\[#([^\|\]]+)(?:\|([^\]]+))?\]\]")


def convert_wikilinks(md_text, slugify_fn):
    def repl(m):
        target = m.group(1).strip()
        label = (m.group(2) or target).strip()
        return f"[{label}](#{slugify_fn(target, '-')})"

    return WIKILINK_RE.sub(repl, md_text)


# Obsidian callouts: "> [!type]- Title" (collapsed) or "> [!type]+ Title" / no sign (expanded),
# followed by "> body" lines. Becomes <details class="callout">, keeping the collapsed state.
CALLOUT_RE = re.compile(r"^>\s?\[!([\w-]+)\]([-+]?)[ \t]*(.*)\n((?:^>.*\n?)*)", re.MULTILINE)


def convert_callouts(md_text, markdown_mod, saved_code=()):
    placeholders = {}

    def repl(m):
        ctype, fold, title, body_block = m.groups()
        title = html_lib.escape(restore_code(title.strip(), saved_code) or ctype.capitalize())
        body_lines = []
        for line in body_block.split("\n"):
            if line.startswith("> "):
                body_lines.append(line[2:])
            elif line.startswith(">"):
                body_lines.append(line[1:])
        body_md = restore_code("\n".join(body_lines).strip("\n"), saved_code)
        body_html = markdown_mod.markdown(
            body_md, extensions=["tables", "fenced_code", "sane_lists", "nl2br"]
        )
        body_html = WRAP_TABLE.sub(r'<div class="table-wrap">\1</div>', body_html)
        open_attr = "" if fold == "-" else " open"
        key = f"@@CALLOUT_{len(placeholders)}@@"
        placeholders[key] = (
            f'<details class="callout"{open_attr}><summary>{title}</summary>'
            f'<div class="callout-body">{body_html}</div></details>'
        )
        return key + "\n\n"

    return CALLOUT_RE.sub(repl, md_text), placeholders


def strip_frontmatter(md_text):
    """Remove YAML frontmatter. A block between two --- lines counts only if it is empty or has a
    `key: value` line, so a note that simply starts with a horizontal rule keeps its content."""
    if md_text.startswith("---"):
        m = re.match(r"^---[ \t]*\n((?:.*?\n)?)---[ \t]*(?:\n|$)", md_text, re.DOTALL)
        if m and (not m.group(1).strip() or re.search(r"^[A-Za-z0-9_-]+:", m.group(1), re.MULTILINE)):
            return md_text[m.end():]
    return md_text


# Code is set aside before the Obsidian conversions and put back afterwards, so examples of
# [[#links]] or > [!callouts]  inside code stay as written. Fences inside a callout ("> ```") are not
# set aside, because the callout needs its "> " lines intact.
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?^\1\2[ \t]*$", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def protect_code(md_text):
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return "\x00CODE%d\x00" % (len(saved) - 1)

    md_text = FENCE_RE.sub(keep, md_text)
    md_text = INLINE_CODE_RE.sub(keep, md_text)
    return md_text, saved


def restore_code(text, saved):
    return re.sub(r"\x00CODE(\d+)\x00", lambda m: saved[int(m.group(1))], text)


PAGE_JS = """
(function(){
  var btn=document.getElementById('to-top');
  function t(){ if(window.scrollY>window.innerHeight) btn.classList.add('show'); else btn.classList.remove('show'); }
  window.addEventListener('scroll',t,{passive:true});
  window.addEventListener('resize',t,{passive:true});
  btn.addEventListener('click',function(){ window.scrollTo({top:0,behavior:'smooth'}); });
  t();
})();
/* The second frozen column starts where the first one ends, whatever its width. */
(function(){
  function syncFrozen(){
    document.querySelectorAll('.table-wrap table').forEach(function(tb){
      var head=tb.querySelector('tr > *:first-child');
      if(!head) return;
      var w=Math.ceil(head.getBoundingClientRect().width);
      tb.querySelectorAll('tr > *:nth-child(2)').forEach(function(c){ c.style.left=w+'px'; });
    });
  }
  syncFrozen();
  window.addEventListener('resize',syncFrozen,{passive:true});
  window.addEventListener('load',syncFrozen);
})();
"""


def build_html(md_text, title, css, lang):
    import markdown
    from markdown.extensions.toc import slugify_unicode

    md_text = strip_frontmatter(md_text)
    if not md_text.endswith("\n"):
        md_text += "\n"  # a callout on the last line still needs its line ending to be found
    md_text, saved_code = protect_code(md_text)
    md_text = convert_wikilinks(md_text, slugify_unicode)
    md_text, callouts = convert_callouts(md_text, markdown, saved_code)
    md_text = restore_code(md_text, saved_code)
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
        extension_configs={"toc": {"slugify": slugify_unicode}},
    )
    for key, block in callouts.items():
        body = body.replace(f"<p>{key}</p>", block).replace(key, block)
    body = WRAP_TABLE.sub(r'<div class="table-wrap">\1</div>', body)
    return f"""<!DOCTYPE html>
<html lang="{html_lib.escape(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(title)}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
{body}
</div>
<button id="to-top" aria-label="Back to top" title="Back to top">&uarr;</button>
<script>{PAGE_JS}</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Convert a Markdown file to a self-contained HTML preview.")
    ap.add_argument("src", help="path to the .md file")
    ap.add_argument("--out", help="output .html path (default: next to the .md)")
    ap.add_argument("--theme", default="default", help="theme name in assets/themes/, or a path to a .css file")
    ap.add_argument("--lang", default="en", help="value of <html lang> (default: en)")
    args = ap.parse_args()

    log("start")
    src = os.path.expanduser(args.src)
    if not os.path.isfile(src):
        log(f"error: input file not found: {src}")
        sys.exit(1)
    if not src.lower().endswith(".md"):
        log(f"warning: input is not a .md file ({src}), converting anyway")
    dst = os.path.expanduser(args.out) if args.out else os.path.splitext(src)[0] + ".html"

    try:
        import markdown  # noqa: F401
    except ImportError:
        log("error: python-markdown is not installed. Run: python3 -m pip install --user markdown")
        sys.exit(1)

    try:
        css = load_css(args.theme)
    except FileNotFoundError as e:
        log(f"error: {e}")
        sys.exit(1)

    log(f"reading {src}")
    try:
        with open(src, encoding="utf-8") as f:
            md_text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        log(f"error: cannot read {src} as UTF-8 text: {e}")
        sys.exit(1)
    title = os.path.splitext(os.path.basename(src))[0]

    log(f"converting with theme '{args.theme}'")
    page = build_html(md_text, title, css, args.lang)

    log(f"writing {dst}")
    try:
        with open(dst, "w", encoding="utf-8") as f:
            f.write(page)
    except OSError as e:
        log(f"error: cannot write {dst}: {e} (does the folder exist?)")
        sys.exit(1)
    log("done")
    print(dst)


if __name__ == "__main__":
    main()
