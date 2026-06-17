# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal macOS dotfiles. Config files live here and are **symlinked** into their expected locations (`~/.zshrc`, `~/.config/nvim`, etc.). Editing a file here updates the live config directly — there is no build or install step, and no application code to compile or test.

## Commands

- `./setup.sh` — the only "test" in the repo. Verifies every brew package/cask is installed and every symlink points at the correct target in this repo. Run it after adding a dependency or symlink. Exits non-zero on any missing package or mispointed link.
- New-machine bootstrap (brew installs, Oh My Zsh, symlink creation) is documented step-by-step in `README.md` under "New Machine Setup".

## Critical invariant: keep three places in sync

When you add a tool, config file, or symlink, update **all three** or `setup.sh` and future setups will drift:

1. **`README.md`** — the `brew install` list (step 2) and the `ln -s` list (step 5) under "New Machine Setup".
2. **`setup.sh`** — `brew_packages` / `brew_casks` arrays in `check_packages`, and the parallel `link_paths` + `targets` arrays in `check_symlinks` (these two arrays are index-matched — add to both at the same position).
3. The actual config file in this repo.

Also: when adding a command or keybind, update the relevant Knowledge Base file at `/Volumes/NO_NAME/knowledge_base/` (see global CLAUDE.md).

## Neovim architecture (`nvim/`)

- `init.lua` requires three user modules in order: `user.options`, `user.keymaps`, `user.lazy`.
- `lua/user/lazy.lua` bootstraps **lazy.nvim** and imports the entire `lua/plugins/` directory. Plugin updates are checked automatically (`checker.enabled = true`).
- **Each file in `lua/plugins/` returns a lazy.nvim spec table** (one plugin or plugin group per file). To add a plugin, create a new file there — it's auto-imported, no central registry to edit.
- `lua/user/keymaps.lua` holds global keymaps; leader is `<Space>`. Notable custom logic: `smart_resize` (walks `winlayout()` to resize on the correct axis, `<leader>m`/`<leader>n`).
- `ftplugin/<filetype>.lua` holds per-filetype buffer-local maps (e.g. `json.lua` binds `<C-f>` to `:%!jq .`). Some depend on external CLIs (`jq`).
- `lazy-lock.json` pins plugin versions — commit it when plugins change.

## Claude config (`claude/`)

Symlinked to `~/.claude/`. `claude/CLAUDE.md` is the **global** user instructions file (applies to all projects, not just this repo). `claude/skills/` and `claude/agents/` are symlinked as directories; some skills inside are themselves symlinks to `~/.agents/skills/`.
