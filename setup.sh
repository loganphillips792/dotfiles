#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

DOTFILES="$HOME/dotfiles"

pass() { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }

ERRORS=0

# --- Package checks ---
check_packages() {
  echo "Checking packages..."

  local brew_packages=(neovim jq tmux imagemagick eza zoxide bat asciiquarium lazygit fzf ranger ripgrep gh)
  for pkg in "${brew_packages[@]}"; do
    if brew list "$pkg" &>/dev/null; then
      pass "$pkg"
    else
      fail "$pkg not installed (brew install $pkg)"
    fi
  done

  # Cask
  if brew list --cask wezterm &>/dev/null; then
    pass "wezterm (cask)"
  else
    fail "wezterm not installed (brew install --cask wezterm)"
  fi

  # Font
  if brew list --cask font-meslo-lg-nerd-font &>/dev/null; then
    pass "font-meslo-lg-nerd-font"
  else
    fail "font-meslo-lg-nerd-font not installed (brew install font-meslo-lg-nerd-font)"
  fi

  # Oh My Zsh
  if [[ -d "$HOME/.oh-my-zsh" ]]; then
    pass "Oh My Zsh"
  else
    fail "Oh My Zsh not installed"
  fi

  # Powerlevel10k
  if [[ -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]]; then
    pass "powerlevel10k theme"
  else
    fail "powerlevel10k not installed"
  fi

  # Zsh plugins
  local zsh_plugins=(zsh-syntax-highlighting zsh-autosuggestions zsh-bat)
  for plugin in "${zsh_plugins[@]}"; do
    if [[ -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/$plugin" ]]; then
      pass "$plugin"
    else
      fail "$plugin not installed"
    fi
  done

  # zsh-autocomplete (separate install)
  if [[ -d "$HOME/zshrc-plugins/zsh-autocomplete" ]]; then
    pass "zsh-autocomplete"
  else
    fail "zsh-autocomplete not installed"
  fi
}

# --- Symlink checks ---
check_symlinks() {
  echo ""
  echo "Checking symlinks..."

  local link_paths=(
    "$HOME/.zshrc"
    "$HOME/.vimrc"
    "$HOME/.config/nvim"
    "$HOME/.tmux.conf"
    "$HOME/.wezterm.lua"
    "$HOME/Library/Application Support/Code/User/keybindings.json"
    "$HOME/Library/Application Support/Code/User/settings.json"
    "$HOME/.claude/settings.json"
    "$HOME/.claude/CLAUDE.md"
    "$HOME/.claude/skills"
    "$HOME/.claude/agents"
  )

  local targets=(
    "$DOTFILES/.zshrc"
    "$DOTFILES/.vimrc"
    "$DOTFILES/nvim"
    "$DOTFILES/tmux/.tmux.conf"
    "$DOTFILES/wezterm-config/.wezterm.lua"
    "$DOTFILES/vscode/keybindings.json"
    "$DOTFILES/vscode/settings.json"
    "$DOTFILES/claude/settings.json"
    "$DOTFILES/claude/CLAUDE.md"
    "$DOTFILES/claude/skills"
    "$DOTFILES/claude/agents"
  )

  for i in "${!link_paths[@]}"; do
    local link="${link_paths[$i]}"
    local target="${targets[$i]}"
    if [[ -L "$link" ]]; then
      local actual
      actual=$(readlink "$link")
      if [[ "$actual" == "$target" ]]; then
        pass "$link -> $target"
      else
        fail "$link points to $actual (expected $target)"
      fi
    elif [[ -e "$link" ]]; then
      warn "$link exists but is not a symlink"
      ERRORS=$((ERRORS + 1))
    else
      fail "$link missing (ln -s $target $link)"
    fi
  done
}

# --- Run ---
check_packages
check_symlinks

echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo -e "${GREEN}All checks passed!${NC}"
else
  echo -e "${RED}$ERRORS issue(s) found.${NC}"
  exit 1
fi
