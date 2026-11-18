# Changelog

## 1.0 (2026-11-18)
- Initial public release.
- Converts one Markdown file into a self-contained HTML page: CSS and the page script are inlined, so it works offline.
- Wide tables scroll sideways, with the header row and the first two columns fixed. Phones get a tighter layout with the columns released.
- Converts two Obsidian syntaxes: `[[#Heading]]` links and `> [!type]-` / `> [!type]+` / `> [!type]` callouts (type names may contain hyphens), which become collapsible blocks that keep their collapsed or open state; no sign starts open.
- `--theme` accepts a theme name with or without `.css`, or a path to your own file.
- A note that starts with a horizontal rule is not mistaken for frontmatter.
- Removes YAML frontmatter and adds a back-to-top button.
- Obsidian syntax inside code blocks and inline code is left as written.
- Read and write errors are logged with a clear message instead of a Python traceback.
- Themes: layout lives in `assets/base.css`, colors and fonts in small files under `assets/themes/`. Ships with `default` and `dark`. A new theme is a new CSS file; the script does not change.
- Optional `settings.md` for the default theme and page language.
