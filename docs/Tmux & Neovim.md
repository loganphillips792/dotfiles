
- My Typical Development Set up
	- One Tmux Window - Vertical Split (Claude Code on left and Neovim on right)
	- One Tmux Window - Horizontal Split (Docker build on top, normal terminal on bottom)

- Switch between windows `Ctrl + a, n`

# Most Commonly Used

## Tmux

- `Ctrl + a, q` — Flash pane numbers — press a number to jump to that pane
- `Ctrl + a, n` — Next window
- `Ctrl + a, p` — Previous window
- `Ctrl + a, c` — Create new window **(MOST_USED)**
- `Ctrl + a, w` — List windows **(MOST_USED)**
- `Ctrl + a, n` — Next window **(MOST_USED)**
- `Ctrl + a, %` — Split vertically  **(MOST_USED)**

## Neovim

- `gd` — Go to definition (via Telescope) 
- `Ctrl-o` — Jump back through jumplist
- gi - view implementations
- `:Telescope keymaps` — List normal mode keymappings
- `<num>gg` — Go to line `<num>` (normal mode, e.g. `42gg`)  **(MOST_USED)**
- `Ctrl-o` — Jump back through jumplist (built-in) **(MOST_USED)**
- `Ctrl-i` — Jump forward through jumplist (built-in) **(MOST_USED)**
- `<leader><num>` — Go to window `<num>` _(custom)_ **(MOST_USED)**



# Neovim / Vim Cheatsheet

---

## Navigation & Movement

- `h` — Move cursor left
- `j` — Move cursor down
- `k` — Move cursor up
- `l` — Move cursor right
- `gg` — Go to top of file
- `G` (`Shift + g`) — Go to bottom of file
- `w` — Jump forward to start of next word
- `e` — Jump to end of current or next word
- `W` — Jump forward to start of next WORD (ignores symbols/punctuation)
- `b` — Jump backward to start of previous word
- `ge` — Jump backward to end of previous word
- `B` — Jump backward to start of previous WORD (ignores symbols/punctuation)
- `<num>w` — Jump forward `<num>` words (e.g. `3w` jumps three words forward)
- `0` — Go to beginning of line
- `:<line-number>` — Go to specific line number (command mode)
- `<num>G` — Go to line `<num>` (normal mode, e.g. `42G`)
- `<num>gg` — Go to line `<num>` (normal mode, e.g. `42gg`)  **(MOST_USED)**
- `Ctrl-o` — Jump back through jumplist (built-in) **(MOST_USED)**
- `Ctrl-i` — Jump forward through jumplist (built-in) **(MOST_USED)**
- `:jumps` — Show the jumplist (list of positions you've jumped to/from)

---

## Editing

- `ciw` — Change inner word — deletes the word under cursor (regardless of cursor position within it) and enters Insert mode
- `caw` — Change around word — deletes the word and the trailing space, enters Insert mode
- `dw` — Delete from cursor to start of next word
- `ce` — Change from cursor to end of word (deletes and enters Insert mode)
- `d<num>w` — Delete the next `<num>` words (e.g. `d2w` deletes two words)
- `dd` — Cut (delete) entire line
- `<num>dd` — Delete `<num>` lines (e.g. `3dd` deletes the current line and the two below)
- `d0` — Delete from cursor to beginning of line
- `d$` — Delete from cursor to end of line
- `dG` — Delete from cursor to end of file
- `ggdG` — Delete all text in file
- `u` — Undo
- `Ctrl + r` — Redo
- `:%s/ANNOTATION//g` - Find all instances of 'ANNOTATION' in the file and delete them
- `:g/^$/d` — Delete all empty lines (no characters)
- `:g/^\s*$/d` — Delete all empty lines (including ones with hidden spaces/tabs)

---

## Visual Mode / Copy / Cut / Paste

- `v` — Enter visual mode (select from cursor)
- `V` — Enter visual line mode (select entire lines)
- `Ctrl + v` — Enter visual block mode
- `y` — Yank (copy) selection
- `d` — Cut (delete) selection
- `p` — Paste after cursor
- `P` — Paste before cursor
- `yy` — Yank entire line
- `<num>yy` — Yank `<num>` lines
- `y$` — Yank from cursor to end of line
- `y^` — Yank from cursor to start of line
- `ggVG` — Select entire file
- `ggyG` — Copy entire file (go to first line, yank to last line)
- `ggVGy` — Copy entire file (visual line select all, yank)
- `:%y+` — Copy entire file to system clipboard

---

## Search

- `/` — Search forward — type pattern, press Enter, then `n` for next / `N` for previous **(MOST_USED)**
- `?` — Search backwards
- `*` — Search forward for the exact word under the cursor. Use `n`/`N` to navigate matches
- `#` — Search backward for the exact word under the cursor
- `g*` — Search forward for the string under the cursor (partial word matches too)
- `<Esc>` — Clear search highlight (`:nohl`) _(custom)_

---

## Search & Replace (Substitute)

Syntax: `:[range]s/pattern/replacement/[flags]`

- `:s/foo/bar/` — Replace first `foo` on current line
- `:s/foo/bar/g` — Replace all `foo` on current line
- `:%s/foo/bar/g` — Replace all `foo` in entire file
- `:%s/foo/bar/gc` — Same, but confirm each replacement
- `:%s/foo/bar/gI` — Case-sensitive (force)
- `:%s/foo/bar/gi` — Case-insensitive (force)
- `:5,20s/foo/bar/g` — Replace in lines 5–20
- `:'<,'>s/foo/bar/g` — Replace in visual selection (select first, then `:s`)
- `:%s/\<foo\>/bar/g` — Match whole word only
- `:%s/foo/bar/gn` — Count matches without replacing
- `:%s//bar/g` — Empty pattern reuses last search (combine with `*` on word under cursor)
- `:%s/foo/bar/g | %s/baz/qux/g` — Chain multiple substitutions

### Project-wide (quickfix workflow)

- `<leader>sg` then `Ctrl + q` — Send grep results to quickfix
- `:cdo s/foo/bar/g | update` — Apply substitution across all quickfix files and save

### Flags

- `g` — All matches on each line (without it, only first)
- `c` — Confirm each replacement
- `i` / `I` — Case-insensitive / case-sensitive
- `n` — Count matches, don't replace

See also: `## grug-far (Search & Replace)` for interactive cross-file UI

---

## Window Splits

### Opening Splits

- `<leader>|` — Vertical split _(custom)_
- `<leader>-` — Horizontal split _(custom)_
- `:vsplit` / `:vsp` — Vertical split
- `Ctrl + w, v` — Vertical split
- `:split` / `:sp` — Horizontal split
- `Ctrl + w, s` — Horizontal split
- `:vsp <file_path>` — Vertical split, open file in new window
- `:sp <file_path>` — Horizontal split, open file in new window

### Navigating Splits

- `Ctrl + w, l` — Move to window on the right
- `Ctrl + w, h` — Move to window on the left (includes file explorer)
- `Ctrl + w, k` — Move to window above
- `Ctrl + w, j` — Move to window below
- `<leader><num>` — Go to window `<num>` _(custom)_ **(MOST_USED)**

### Resizing Splits

- `Ctrl + w, i` — Maximize current vertical split
- `Ctrl + w, _` — Maximize current horizontal split
- `Ctrl + w, =` — Reset all splits to equal size
- `:<width>vsp` — Set custom width for vertical split
- `:<height>sp` — Set custom height for horizontal split
- `<leader>m` — Expand current window (smart: vertical or horizontal) _(custom)_
- `<leader>n` — Shrink current window (smart: vertical or horizontal) _(custom)_
- `Ctrl + Up` — Increase height by 2 _(custom)_
- `Ctrl + Down` — Decrease height by 2 _(custom)_
- `Ctrl + Left` — Decrease width by 2 _(custom)_
- `Ctrl + Right` — Increase width by 2 _(custom)_

---

## Tabs

- `:tabnew` — Open new tab
- `:tabnew <filename>` — Open file in new tab
- `:tabclose` — Close current tab
- `:tabclose N` — Close tab number N
- `gt` — Next tab
- `gT` — Previous tab
- `Ngt` — Go to tab number N
- `:tabs` — List all open tabs

---

## File Operations

- `:e <filename>` — Create or open file
- `:e <path>/filename.ext` — Open file by full path
- `:e` or `:edit` — Reload current file from disk (single buffer)
- `:e!` — Discard unsaved local changes and force reload from disk
- `:Lexpl` — Open file explorer on left side
- `:Lex 30` — Open file explorer with width of 30
- `:!rm %` — Delete currently opened file (shell execution)
- `:qa` — Quit all windows

### Copy File Path to System Clipboard

`@+` is the `+` register (system clipboard, requires `has('clipboard')`).

| Command | Copies |
|-|-|
| `:let @+ = expand("%:p")` | Absolute path |
| `:let @+ = expand("%")` | Path relative to cwd |
| `:let @+ = expand("%:p:h")` | Containing directory |
| `:let @+ = expand("%:t")` | Filename only |

- `<leader>cpp` — Copy absolute path of current file to system clipboard _(custom)_

---

## LSP & Code Intelligence

Code navigation keybinds like `gd` (go to definition) come from **nvim-lspconfig** (`nvim/lua/plugins/lsp-config.lua`), not directly from the language servers themselves.

How it works: `nvim-lspconfig` configures language servers (gopls, pyright, vtsls, lua_ls, etc.) and the servers do the actual analysis — finding definitions, references, types, diagnostics. The keymaps are registered inside an `LspAttach` autocmd, so they're only active in buffers where an LSP has attached. Many keybinds route through Telescope (e.g. `gd` → `:Telescope lsp_definitions`) so results appear in a fuzzy-searchable picker instead of jumping blindly.

| Keybind | Action |
|-|-|
| `gd` | Show LSP definitions (Telescope) |
| `gD` | Go to declaration |
| `gR` | Show LSP references (Telescope) |
| `gi` | Show LSP implementations (Telescope) |
| `gt` | Show LSP type definitions (Telescope) |
| `gpd` | Peek definition in a floating window (`q` to close) _(custom)_ |
| `K` | Show hover documentation for symbol under cursor |
| `<leader>ca` | Show available code actions (normal + visual) |
| `<leader>rn` | Smart rename symbol |
| `<leader>d` | Show line diagnostics in float |
| `<leader>D` | Show all buffer diagnostics (Telescope) |
| `[d` | Jump to previous diagnostic |
| `]d` | Jump to next diagnostic |
| `<leader>rs` | Restart LSP (`:LspRestart`) |
| `<leader>fm` | Format buffer (or visual selection) via LSP/none-ls |
| `<leader>ch` | Switch between C/C++ source and header (clangd only) |

After jumping with `gd`/`gD`/`gi`/`gt`, use `Ctrl-o` to jump back and `Ctrl-i` to jump forward through the jumplist.

### Other LSP workflows

- `grn` — Rename (built-in, Neovim 0.10+). Type the new name, press Enter — updates all instances in the file and across the module
- `Ctrl-w v` then `gd` — Open definition in a vertical split
- `Ctrl-w s` then `gd` — Open definition in a horizontal split
- `Ctrl-w }` — Open definition in a preview window at the top of the screen
- `:ptag` — Open definition in preview window (when using tags)
- `:lua vim.lsp.buf.format()` — Format current buffer via LSP. Only ever formats the current buffer; there's no built-in "format whole project" from inside Neovim — use the formatter's CLI instead (e.g. `:!ruff format .`, then `:checktime` to reload open buffers)
- `:LspRestart ruff` — Restart a single language server by name (e.g. after changing its config); `:LspRestart` with no argument restarts all attached servers
- `:help lspconfig-all` — View all lspconfig documentation

---

## Telescope

- `<leader>sf` — Search files
- `<leader>sg` — Live grep
- `<leader>sw` — Grep word under cursor
- `<leader>sh` — Search help tags
- `<leader>sk` — Search keymaps
- `<leader>ss` — Telescope builtin picker
- `<leader>sd` — Search diagnostics
- `<leader>sr` — Resume last search
- `<leader>s.` — Recent files
- `<leader><leader>` — Find open buffers
- `<leader>gb` — Git branches
- `:Telescope find_files` — Find files
- `:Telescope live_grep` — Live grep
- `:Telescope keymaps` — List normal mode keymappings
- `:Telescope help_tags` — Search help tags
- `:Telescope builtin` — Browse all Telescope pickers
- `:Telescope buffers` — List open buffers
- `:help Telescope` — Open Telescope help

### Git

- `<leader>gs` — Git status (stage/unstage files with diff preview)
- `<leader>gc` — Git commits (browse commit log)
- `<leader>gb` — Git branches (switch branches)
- `<leader>gt` — Git stash (browse stash entries)

### Live Grep to Quickfix Workflow

- `<leader>sg` — Open live grep
	- Live grep uses **ripgrep**, which interprets patterns as **regex** by default
	- Special characters like `(`, `)`, `[`, `{` must be escaped with `\`
	- Example: to search for `run_scan(`, type `run_scan\(`

> **Why you have to escape `(` in live grep:** `<leader>sg` runs Telescope's `live_grep`, which passes your input to ripgrep as a **regex**, not a literal string. In regex, `(` and `)` are grouping metacharacters, so ripgrep tries to interpret `(foo)` as a capture group. To match a literal parenthesis you have to escape it: `\(`. Same goes for other regex metacharacters: `.`, `*`, `+`, `?`, `[`, `]`, `{`, `}`, `|`, `^`, `$`, `\`.
>
> To search literally without escaping, pass `--fixed-strings` (`-F`) to ripgrep, or use `grep_string` / the `telescope-live-grep-args` extension.
- `Ctrl + q` — Send all results to the quickfix list
- `<Tab>` / `<S-Tab>` — Multi-select individual items
- `Alt + q` — Send only selected items to the quickfix list
- `:copen` — Open the quickfix list
- `:cnext` / `:cprev` — Navigate quickfix entries

---

## Snacks

- `<leader>/` — Grep
- `<leader>:` — Command history
- `<leader>fr` — Recent files
- `<leader>e` — Open file explorer
- `<leader>l` — Open Lazygit _(requires `brew install lazygit`)_
- `<leader>gB` — Git blame line
- `:lua Snacks.picker.grep()` — Activate Snacks picker
- `:lua Snacks.dashboard()` — Open the Snacks dashboard

---

## Neo Tree

- `:Neotree` — Open Neo Tree (`?` inside to view list of mappings)
- `:Neotree position=current` — Open Neo Tree in current window
- `:Neotree toggle` — Toggle Neo Tree

---

## nvim-tree

- Highlight a file, then:
    - `a` — Add (create) a new file
    - `r` — Rename file
    - `d` — Delete file

---

## oil.nvim

- `-` — Activate oil.nvim (opens parent directory of current file as a buffer)
- `dd` then `:w` — Delete a file (delete the line, then save)
- Create a new line in insert mode to create directory
- Edit filename as normal text (e.g. `ciw`, `A`) then `:w` — Rename a file on the filesystem

---

## VimTeX (LaTeX)

- **Plugin**: `lervag/vimtex` — configured in `plugins/vimtex.lua`
- **LSP**: `texlab` — configured in `lsp-config.lua`, installed via Mason
- **Dependencies**: `brew install --cask mactex skim`

### Compilation

- `\ll` — Start/stop continuous compilation (latexmk)
- `\lv` — Forward search to Skim (jump to PDF location)
- `\le` — View errors/warnings
- `\lk` — Stop compilation
- `\lc` — Clean auxiliary files
- `:VimtexInfo` — Show vimtex status (compiler, viewer, TeX distribution)

### Build & View Workflow

Example `deriv.tex`:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Derivative of $5x^5$}

Using the power rule $\frac{d}{dx} x^n = n x^{n-1}$:

\begin{align*}
\frac{d}{dx}\left(5x^5\right) &= 5 \cdot \frac{d}{dx}\left(x^5\right) \\
                              &= 5 \cdot 5x^{4} \\
                              &= 25x^4
\end{align*}

\end{document}
```

1. Run `nvim deriv.tex`.
2. Press `\ll` to start continuous compilation. latexmk recompiles every time you save and opens the PDF in Skim.
3. Press `\lv` to jump to the matching spot in the PDF. `Cmd+Shift+Click` in Skim jumps back to Neovim.
4. If it fails, press `\le` to see the errors. When you're done, `\lc` deletes the extra build files.

### Editing (tex filetype)

- `Ctrl+L` (insert mode) — Fix previous spelling mistake without leaving insert _(custom)_
- Concealment on (level 2) — e.g. `\alpha` renders as symbol
- Word wrap + linebreak enabled

### Spell Check

- Enabled automatically for `.tex` files (`en_us`)
- `]s` — Jump to next misspelled word
- `[s` — Jump to previous misspelled word
- `z=` — Show spelling suggestions for word under cursor
- `zg` — Add word under cursor to spellfile (mark as good)
- `zw` — Mark word as wrong (add to bad-word list)
- `zug` — Undo `zg` (remove from spellfile)
- `:set spell` / `:set nospell` — Toggle spell check manually

### Skim Reverse Search (PDF → Neovim)

- `Cmd+Shift+Click` in Skim — jump back to corresponding line in Neovim
- Requires Skim Preferences → Sync → set editor to nvim

### Snippets

- Custom LaTeX snippets: `nvim/luasnippets/tex.lua`
- Loaded via LuaSnip's `from_lua` loader in `completions.lua`

### Troubleshooting

- `:LspInfo` — Verify texlab is attached
- `:VimtexInfo` — Check vimtex detects TeX distribution
- `:checkhealth` — Run general health checks
- `:TSInstallInfo` — Verify `latex` treesitter parser is installed

---

## clangd (C/C++ LSP)

- Configured in `lsp-config.lua` (`servers.clangd`), installed via Mason; `cpp` treesitter parser added
- Flags: `--background-index` (indexes whole project for cross-file refs), `--clang-tidy` (lint diagnostics), `--header-insertion=iwyu` (auto-adds `#include` on completion)
- **Needs `compile_commands.json`** at the project root (or `build/`) to know include paths/flags. Generate with CMake: `cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`, or for Make: `bear -- make`. For tiny projects a `compile_flags.txt` (one flag per line, e.g. `-std=c++20`) works instead
- `<leader>ch` / `:LspClangdSwitchSourceHeader` — toggle `.cpp` ↔ `.h`
- `:LspClangdShowSymbolInfo` — show info for the symbol under cursor
- **Format on save** via the standalone `clang-format` (installed by Mason, run through none-ls); clangd's own formatting is disabled so they don't both run. Reads `.clang-format` if present, else LLVM style. Skip once with `:noautocmd w`
- Global style: `~/.clang-format` → `dotfiles/.clang-format` (Google, made with `clang-format --style Google --dump-config > .clang-format`). clang-format walks up parent dirs for a config, so it applies to anything under `~`; a project's own `.clang-format` wins
- Mason's `bin/` is appended to `$PATH` in `.zshrc`, so `clang-format -i src/*.cpp` works from the terminal too

### Debugging C/C++ (nvim-dap + codelldb)

Configured in `plugins/dap.lua`. Loads at startup (`event = "VeryLazy"`), so no keypress is needed to activate it. `codelldb` is installed at startup by mason-tool-installer (`plugins/mason.lua`); `mason-nvim-dap` registers its adapter and default launch configs (`handlers = {}`); `nvim-dap-ui` opens automatically when a session starts and closes when the program exits. **Compile with debug symbols first** (`-g`, or `-DCMAKE_BUILD_TYPE=Debug`). On `<leader>bc` pick "LLDB: Launch" (or "LLDB: Launch (args)" to pass arguments) and enter the path to the binary.

| Keybind | Command | Action |
|-|-|-|
| `<leader>bb` | `:DapToggleBreakpoint` | Toggle breakpoint |
| `<leader>bc` | `:DapContinue` | Start / continue |
| `<leader>bn` | `:DapStepOver` | Step over (next) |
| `<leader>bi` | `:DapStepInto` | Step into |
| `<leader>bo` | `:DapStepOut` | Step out |
| `<leader>bq` | `:DapTerminate` | Terminate session |
| `<leader>bu` | `:lua require("dapui").toggle()` | Toggle debugger UI |

Using `<leader>b*` rather than `<leader>d*` (common in tutorials) because `<leader>d` is already taken by the diagnostics float and Dirbuf.

---

## Ruff (Python LSP)

- Ruff handles linting, formatting, and import organizing. Pyright stays for type checking and hover docs.
- Ruff's hover is disabled in favor of Pyright (configured in `lsp-config.lua`)
- `<leader>ca` — Code actions (auto-fix lint issues, organize imports)
- `:lua vim.lsp.buf.format()` — Format current buffer via Ruff
- By default, Ruff writes logs to stderr, available in Neovim's LSP client log file: `:lua vim.print(vim.lsp.get_log_path())`
- To view trace logs between Neovim and Ruff, set the LSP client log level: `vim.lsp.set_log_level('debug')`
- Commands come from the LSP protocol — Ruff's server advertises capabilities when it attaches:
    - Diagnostics — pushes lint warnings/errors automatically (`textDocument/publishDiagnostics`)
    - Code actions (`<leader>ca`) — auto-fix, organize imports (`textDocument/codeAction`)
    - Formatting (`:lua vim.lsp.buf.format()`) — `textDocument/formatting`
- No manual command registration — Neovim's LSP client reads Ruff's capabilities and maps them to `vim.lsp.buf.*` functions and your existing LSP keybinds in `lsp-config.lua`
- `:lua vim.print(vim.lsp.get_clients({name='ruff'})[1].server_capabilities)` — View Ruff's reported capabilities

---

## Mason

- `:Mason` — View installed and available packages
- `:MasonUpdate` — Update Mason registry
- `:MasonInstallAll` — Install all configured packages

---

## lazy.nvim

- `:Lazy install` — Install plugins
- `:Lazy check` — Check for plugin updates
- `:Lazy update` — Update plugins. Updates the lock file
- `:Lazy update telescope.nvim` - Update specific plugin
- `:Lazy sync` — Sync (install, clean, update)
- `:Lazy restore` - update all your plugins to the version from the lockfile
- `:Lazy profile`
- `:Lazy clean` - Clean plugins that are no longer needed
- 

---
## Neoscroll (Smooth Scrolling)

- **Plugin**: `karb94/neoscroll.nvim` — configured in `plugins/neoscroll.lua`
- Adds smooth animated scrolling to built-in Vim scroll commands

### Scrolling Commands (hold Ctrl + tap key)

- `Ctrl + u` — Scroll up half page
- `Ctrl + d` — Scroll down half page
- `Ctrl + b` — Scroll back full page
- `Ctrl + f` — Scroll forward full page
- `Ctrl + y` — Scroll view up one line (cursor stays put)
- `Ctrl + e` — Scroll view down one line (cursor stays put)

### Cursor-to-Screen Position

- `zt` — Move view so current line is at the top
- `zz` — Move view so current line is at the center
- `zb` — Move view so current line is at the bottom

### Debugging

- `:lua print(vim.inspect(require('neoscroll')))` — Check if plugin is loaded
- `:verbose map <C-u>` — Show what's mapped to a key and where it was set
- `:lua require('neoscroll').ctrl_d({ duration = 250 })` — Test scrolling directly (bypasses keybinding)

---
## nvim-ufo (Folding)

- `zo` — Open fold under cursor
- `zc` — Close fold under cursor
- `za` — Toggle fold under cursor
- `zR` — Open all folds
- `zM` — Close all folds
- `zK` — Peek folded lines under cursor
- Uses LSP + indent as fold providers

---
## Csv View

- `:CsvViewToggle` - Enable CSV view with automatic delimiter detection
- `:CsvViewToggle delimiter=, display_mode=border header_lnum=1` - enable with specific settings

---

## grug-far (Search & Replace)

- `:GrugFar` — Open grug-far (command mode)
- `<leader>r` — Open grug-far (search and replace across files)
- `<leader>R` — Search and replace current word under cursor
- (visual) `<leader>r` — Search and replace visual selection
- **Inside grug-far buffer:**
  - `\r` — Apply all replacements (Sync All)
  - `\l` — Apply replacement on current line only (Sync Line)
  - `?` — Show all grug-far keybinds

---

## Formatting & External Commands

- `:%!jq .` — Format JSON in buffer using `jq` (must be installed). `%` = entire buffer, `!` = external program, `.` = jq identity filter. Tip: map in `ftplugin/json.lua` to `Ctrl + f`

---

## Display & Info

- `:set number` — Show line numbers
- `:colorscheme` — Get current color scheme
- `:colorscheme <tab>` — Cycle through available color schemes
- `:map` — List all key bindings
- `:version` — Show Neovim version, build info, and compile flags
- `:checkhealth` — Run health checks
- `:checkhealth vim.deprecated` — Check for deprecated Vim options, mappings, and APIs in your config

---

## Help

- `:help <plugin-name>` — Open help docs for any installed plugin (e.g. `:help telescope`, `:help lazy.nvim`, `:help neo-tree`, `:help grug-far`)
- `:h lua-guide` — Open Lua guide
- `:help nvim-config` — Open Neovim config help
- `:help Telescope` — Open Telescope help

---

## Which-Key

- Press `<leader>` and wait — show available keybindings in a popup
- `<leader>?` — Show buffer-local keymaps
- `<esc>` — Cancel and close the popup
- `<bs>` — Go up one level
- `Ctrl + d` — Scroll down in popup
- `Ctrl + u` — Scroll up in popup
- `:checkhealth which-key` — Run which-key health checks

---

---

# tmux Cheatsheet

---

## Session Management (from shell)

- `tmux ls` — List running sessions
- `tmux new -s <name>` — Create new named session
- `tmux attach -t <name>` — Attach to session by name
- `tmux rename-session -t <old> <new>` — Rename a session
- `tmux switch -t <name>` — Switch to session directly without detaching first
- `tmux kill-session` — End the current session only
- `tmux kill-session -t <name>` — Kill session by name
- `tmux kill-server` — End all sessions and exit the tmux process
- Type `exit` in a pane to kill that pane

---

## Prefix Key

Default prefix is `Ctrl + b`, but this dotfiles config rebinds it to **`Ctrl + a`** _(custom)_. Press `Ctrl + a` twice to send a literal `Ctrl + a` to the running app.

All shortcuts below use `Ctrl + a` as the prefix.

---

## Windows

- `Ctrl + a, c` — Create new window **(MOST_USED)**
- `Ctrl + a, w` — List windows **(MOST_USED)**
- `Ctrl + a, f` — Find windows
- `Ctrl + a, n` — Next window **(MOST_USED)**
- `Ctrl + a, p` — Previous window
- `Ctrl + a, <number>` — Switch to window by number
- `Ctrl + a, ,` — Rename the current window
- `Ctrl + a, !` — Break current pane into its own window
- `Ctrl + a, &` - Kill window

---

## Panes — Splitting

- `Ctrl + a, %` — Split vertically  **(MOST_USED)**
- `Ctrl + a, "` — Split horizontally
- `Alt + n` — New horizontal split _(custom, no prefix needed)_
- `Alt + v` — New vertical split _(custom, no prefix needed)_

---

## Panes — Navigation

- `Ctrl + a, Up/Down/Left/Right` — Switch panes by direction _(custom)_
- `Ctrl + a, o` — Cycle to the next pane
- `Ctrl + a, q` — Flash pane numbers — press a number to jump to that pane

---

## Panes — Resizing & Layout

- `Alt + Up/Down/Left/Right` — Resize pane by 2 _(custom, no prefix needed, hold to repeat)_
- `Ctrl + a, Shift + Up` — Resize pane up by 5 _(custom, repeatable)_
- `Ctrl + a, Shift + Down` — Resize pane down by 5 _(custom, repeatable)_
- `Ctrl + a, Shift + Left` — Resize pane left by 10 _(custom, repeatable)_
- `Ctrl + a, Shift + Right` — Resize pane right by 10 _(custom, repeatable)_
- `Ctrl + a, z` — Toggle zoom (pane takes full window; repeat to restore)
- `Ctrl + a, {` — Move current pane left/up
- `Ctrl + a, }` — Move current pane right/down
- `Ctrl + a, Ctrl + o` — Rotate all panes in current window
- `Ctrl + a, Spacebar` — Cycle through the five standard layouts
- `Ctrl + a, x` - Kill pane

---

## Display Popups

- `tmux display-popup` — Open a popup window overlay (shell command: closes on exit)
- `:display-popup` — Same, from tmux command mode
- `Ctrl + a, y` — Lazygit popup (80×80%, in current pane directory) _(custom)_
- `Ctrl + a, t` — Show clock / current time in the pane
- `Ctrl + a, Ctrl-r` — Ranger popup (90×90%, in current pane directory) _(custom)_
- `Ctrl + a, Ctrl-t` — Zsh shell popup (in current pane directory) _(custom)_
- `Ctrl + a, Ctrl-n` — Create new session (prompts for name) _(custom)_
- `Ctrl + a, j` — Switch session via fzf _(custom)_
- `Ctrl + a, d` — Dotfiles menu (quick open .zshrc, .tmux.conf, .wezterm.lua, nvim config) _(custom)_

---

## Sessions — In-tmux

- `Ctrl + a, d` — Detach from session
- `Ctrl + a, s` — Interactive session list (arrow keys to select, Enter to switch)

---

## Copy Mode (Scrolling & Selection)

Copy mode lets you scroll back through terminal output, search, select text, and copy it.

### Entering & Exiting

- `Ctrl + a, [` — Enter copy mode
- `q` or `Esc` — Exit copy mode

### Navigation (vi-style when `mode-keys vi` is set)

- `h/j/k/l` — Move cursor left/down/up/right
- `Ctrl + u` — Half-page up
- `Ctrl + d` — Half-page down
- `Ctrl + b` — Full page up
- `Ctrl + f` — Full page down
- `g` — Go to top of history
- `G` — Go to bottom of history
- `0` — Beginning of line
- `$` — End of line
- `w` / `b` — Jump forward / backward by word

### Searching

- `/` — Search forward (type pattern, press Enter)
- `?` — Search backward
- `n` — Next match
- `N` — Previous match

### Selecting & Copying

- `Space` — Start selection (vi mode)
- `v` — Start selection (if using `bind -T copy-mode-vi v send -X begin-selection`)
- `V` — Select entire line
- `Enter` or `y` — Copy selection to tmux buffer (and exit copy mode)
- `Ctrl + a, ]` — Paste from tmux buffer

### Copying to System Clipboard

- Requires `copy-pipe-and-cancel` binding, e.g.:
  `bind -T copy-mode-vi y send -X copy-pipe-and-cancel "pbcopy"` _(macOS)_
- With mouse: select text while holding mouse → automatically copies if `set -g mouse on` and clipboard binding is configured

---

## Command Mode

Enter with `Ctrl + a, :` — a yellow bar appears at the bottom. Type a command and press Enter.

- `:new-window -n "my-server"` — Create a named window
- `:rename-window "claude-session"` — Rename current window
- `:kill-session` — Close the entire session
- `:kill-server` — Kill the tmux server and all sessions
- `:kill-pane` — Kill the current pane
- `:set -g mouse on` — Enable mouse support (scrolling, clicking, pane resizing)
- `:resize-pane -D 10` — Increase height (down)
- `:resize-pane -U 10` — Decrease height (up)
- `:resize-pane -R 10` — Increase width (right)
- `:resize-pane -L 10` — Decrease width (left)

---

---

# WezTerm Cheatsheet

`Super` = `Cmd`

---

## Window & Tab Management

- `Super + n` — Open new window
- `Super + t` — Create new tab
- `Super + w` — Close current tab
- `Super + Shift + f` — Toggle fullscreen _(custom)_
- `Super + k` — Clear scrollback and viewport _(custom)_
- `Ctrl + Shift + !` — Move current pane to a new window _(custom)_
- `Cmd + h` — Hide window

---

## Tab Navigation

- `Super + Shift + [` — Previous tab
- `Super + Shift + ]` — Next tab

---

## Fonts

- `wezterm ls-fonts` — Show current font configuration, including face and size
- `wezterm ls-fonts --list-system` — List fonts available for use in your `wezterm.lua`
- `wezterm ls-fonts --text "text"` — Show which fonts/glyphs would be used to render the given text

---

## Mouse / Clipboard

- Selecting text with the mouse **automatically copies it to the clipboard** — this is WezTerm's default `CompleteSelection` mouse binding, not a Claude Code or shell feature. It works in any program (shell, vim, less, Claude Code) since it's the terminal emulator doing the copy on mouse-up.

---

## Copy Mode

- `Ctrl + Shift + X` — Activate copy mode
- `y` — Copy and exit copy mode
- `Esc` — Exit copy mode
- `Shift + V` — Line selection
- `Ctrl + V` — Rectangular selection

### Movement

- `Tab` / `w` — Move forward one word
- `Shift + Tab` / `b` — Move backward one word
- `e` — Move forward one word end _(since 20230320-124340-559cb7b0)_
- `0` — Move to start of this line
- `Enter` — Move to start of next line
- `$` — Move to end of this line

---

---

# Mac OS

- **Hide current app** — `Command (⌘) + H`
- **Hide all other apps** — `Option + Command (⌘) + H`