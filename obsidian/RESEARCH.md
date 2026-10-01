# Tron theme references

Research date: 29 September 2026. Counts below are rounded values displayed by the retrieved pages, which can lag live totals. They are adoption signals, not a synchronized popularity ranking.

## Primary reference for v0.2: your ENCOM Archive OS

The user's existing `encom-obsidian-blog` project takes precedence over the editor-theme shortlist for this revision. Source location: `../encom-boardroom`.

| Observed detail | Local source | Obsidian adaptation |
| --- | --- | --- |
| Pure black, cyan `#00EEEE`, yellow `#FFCC00` | `css/global.css`, `css/light-table-styles.css` | Black application chrome, cyan links, yellow selection edge |
| Teal `#6FC0BA` frames and dark inner borders | `css/light-table-styles.css` `.container-border`, `.content-container`, `.content` | Teal modal/prompt frames, paired divider lines, restrained glow |
| Orange `#FF9933` signal category | `css/boardroom-styles.css` `.header-other2` | Warning callouts and numeric values |
| Inconsolata typography and off-white `#D8E1DD` reader | `js/blog-adapter.js` reader rules | Mono interface labels; off-white notes with optional mono text |
| Thin cyan left rails and yellow active state | `css/blog.css` `.blog-interaction` | Cyan-tinted file selection with a yellow left edge |
| Quiet, constrained article reading | `AGENTS.md`, `.blog-reader-body` | Readable line width and no animated decorations behind notes |

The bundled `images/screenshot_lighttable.jpg` was inspected as a visual reference. It documents the original light-table design, not a fresh capture of the current blog runtime. No changes were made to that project. New CSS adapts the visual ideas to native Obsidian elements; no animation code, artwork, or font files were copied.

## Shortlist

### Version 0.3: Tokyo Night role comparison

The locally installed Tokyo Night 1.1.6 uses yellow for H2, question callouts, and file badges; orange for highlights, warnings, and graph tags. Its bold/italic text uses cyan. These are distinct semantic roles rather than an undifferentiated warm accent.

For Tron Grid, the latest user correction is explicit: the main title stays white, smaller section headings are cyan, and inline highlighting and smaller elements carry yellow/orange and other semantic colors. Accordingly, v0.3 assigns soft gold to bold text, highlights, tags, and strings, and soft amber to inline code and numeric values. Orange warning/graph-tag roles and yellow selection/search markers remain. In v0.3.1, the title/H1 is white, H2/H3 cyan, and H4–H6 pale cyan. These choices adapt the reference rather than copy its heading colors.

| Theme / collection | Platform | Evidence and reason to select |
| --- | --- | --- |
| [Dayle Rees — Tron / Tron Legacy](https://github.com/daylerees/colour-schemes) | Sublime, VS Code, Vim, JetBrains and other editors | The collection has about **9.3k GitHub stars**, across all its themes. It explicitly includes Tron and Tron Legacy and lists JetBrains support. Strong historical starting point; the star count is not specific to Tron. |
| [Tron Color Scheme — Bret Comnes](https://packagecontrol.io/packages/Tron%20Color%20Scheme) | Sublime Text | About **8K installs** on Package Control. A standalone Tron/Tron Legacy fork with established usage. Selected as the clearest theme-specific adoption signal. |
| [Tron Legacy — Bret Comnes](https://marketplace.visualstudio.com/items?itemName=bcomnes.tron-legacy) | VS Code | A hand-edited port, linking back to the Sublime and Atom versions. Selected for cross-editor lineage. The retrieved Marketplace page did not expose a usable install total. |
| [Troning — Tron Legacy Theme Pack](https://marketplace.visualstudio.com/items?itemName=rubenzn.encom-tron-legacy) | VS Code, including integrated terminal ANSI colors | The Encom flavor documents a blue-black UI with cyan, cool foregrounds, and amber/green accents; CLU provides a warmer alternative. Useful for full-interface coverage. Popularity was not established. |
| [Cyberpunk 2019](https://github.com/the-frey/cyberpunk-2019) | Emacs and iTerm2 | About **77 GitHub stars**. The author explicitly calls it a spin on Tron Legacy and Cyberpunk, and includes an `.itermcolors` file. A smaller, adjacent terminal reference, not a widely adopted pure Tron theme. Its terminal palette is tuned for oh-my-zsh/agnoster. |

The JetBrains selection is the historic editor color-scheme collection, not a claim that a maintained Tron plugin skins all of a modern JetBrains IDE. The [JetBrains source directory](https://github.com/daylerees/colour-schemes/tree/master/jetbrains) is linked for inspection; compatibility with a current IDE was not tested.

Additional lineage: [bcomnes/atom-tron-legacy](https://github.com/bcomnes/atom-tron-legacy) and [cparadeise/tron-legacy-ui-atom](https://github.com/cparadeise/tron-legacy-ui-atom). These are historical visual references, not recommendations to switch to Atom.

## Decisions for Obsidian

The initial direction combined the established Tron Legacy family's dark/cyan identity with the fuller interface coverage documented by Troning. The user then supplied their own ENCOM Archive OS as the primary reference. Version 0.2 adopts its exact cyan, teal, yellow, and orange while retaining the requested neon-blue structural accent.

Tron Grid is a new implementation using Obsidian's native styling model. It is not a literal conversion of an upstream theme file. The palette was tuned for readable long-form text and conservative glow rather than copying one source verbatim. Uprising contributes the preference for simple angular edges; no established Uprising-specific editor theme was verified in this search.

- Cyan identifies links, focus, and active navigation.
- Blue organizes headings and code keywords.
- Ice foregrounds keep most prose neutral.
- Orange/yellow appear in warnings, numeric values, strings, and highlights.
- Native errors and success states retain distinguishable red/green colors.

The smaller terminal reference helped establish that a Tron-influenced terminal option exists. Its stronger multicolor character was not adopted as the main Obsidian palette.

## Implementation references

- [Obsidian: About styling](https://docs.obsidian.md/Reference/CSS%20variables/About%20styling) — customize native variables for broad coverage.
- [Obsidian: Build a theme](https://docs.obsidian.md/Themes/App+themes/Build+a+theme) — theme folder, manifest, and appearance selection.
- [Obsidian: Color variables](https://docs.obsidian.md/Reference/CSS%20variables/Foundations/Colors) — native palette roles.
- [Official desktop Appearance settings](https://learn.chatgpt.com/docs/reference/settings#appearance) — future Codex color/font mapping; not proof of an arbitrary CSS import mechanism.

### Version 0.3.2: brighter inline signals

Following the user’s request for stronger orange/yellow, the muted gold and amber were replaced by #FFE600 electric yellow and #FF8C1A vivid orange. Tag borders and inline-code backgrounds/edges were strengthened. White main titles and cyan section headings remain unchanged.

### Version 0.3.3: orange-led warm accents

The user prefers orange as the common warm accent, drawing on military programs, with yellow as the rarer CLU-associated accent. Bold text, tags, strings, inline code, values, active file edges, and question/warning callouts use orange. Yellow is limited to explicit highlights, search matches, and important callouts. White titles and cyan headings are retained.
