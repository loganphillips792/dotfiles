# dotfiles

These are the dofiles I use on Mac OS.

Since we are changing the deafult location of .zshrc and .vimrc, we need to use symlinks:
- `ln -s ~/dotfiles/.zshrc ~/.zshrc` (Now, editing ~/dotfiles/.zshrc will update ~/.zshrc as well)
- `ln -s ~/dotfiles/.vimrc ~/.vimrc`
- `ln -s ~/dotfiles/nvim ~/.config/nvim`
- `ln -s ~/dotfiles/wezterm-config/.wezterm.lua ~/.wezterm.lua`
- `ln -s ~/dotfiles/vscode/keybindings.json ~/Library/Application\ Support/Code/User/keybindings.json`
- `ln -s ~/dotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json`
- `ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf`
- `ln -s ~/dotfiles/claude/settings.json ~/.claude/settings.json`
- `ln -s ~/dotfiles/claude/CLAUDE.md ~/.claude/CLAUDE.md`
- `ln -s ~/dotfiles/claude/skills ~/.claude/skills`
- `ln -s ~/dotfiles/claude/agents ~/.claude/agents`
- `ln -s ~/dotfiles/opencode/opencode.json ~/.config/opencode/opencode.json`

# Zshell

`zsh --version`

`echo $SHELL`

## Setup

If you keep your zshrc somewhere other than your home directory (~), then you wil have to use a symlink. For example, I store my dot files in ~/dotfiles.

When you restart your terminal, you should see your Zshr configured properly

## Oh My ZSH

[Repo Link](https://github.com/ohmyzsh/ohmyzsh/)

- `sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
    - Installs at ~/.oh-my-zsh
    - ls ~/.oh-my-zsh
- themes located at .oh-my-zsh/themes
    - for example: `git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k` (`p10k configure` if configuration wizard does not open after restart)
- To reinstall: Remove `~/.oh-my-zsh` and then run the install command again

- Any plugins from oh-my-zsh you want to use, add to the plugins=() variable
- Zshell plugins: I created a folder `~/zshrc-plugins` and this is where I `git clone` plugins into.
- I am currently using powerlevel10k theme. View the installation instructions [here](https://github.com/romkatv/powerlevel10k#oh-my-zsh). I followed the instructions for 'Oh My ZSH'. It will take you through the "configuration wizard" in order to configure the theme. Ultimtately installs the configuration at ~/.pk10.zsh. Note, this also uses the "Meslo Nerd Font". View the repo to install this font.

`omz update` - Update

### git

https://kapeli.com/cheat_sheets/Oh-My-Zsh_Git.docset/Contents/Resources/Documents/index

### Zsh Autocomplete

Note: You can't add it as a regular oh-my-zsh plugin. Read more here: https://github.com/marlonrichert/zsh-autocomplete?tab=readme-ov-file#keyboard-shortcuts

https://github.com/marlonrichert/zsh-autocomplete?tab=readme-ov-file#keyboard-shortcuts

### Zsh Syntax Highlighting

```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```


### z
 - Enables the use of the z command, which is a tool for jumping to frequently used directories quickly. It keeps track of directories you visit and allows you to navigate to them by typing part of the directory name.
 - Example: If you've visited /usr/local/bin often, typing z bin would quickly take you there.

# Bash

macOS ships with Bash 3.2 (from 2007) due to GPL licensing. To get a modern version, install via Homebrew:

```
brew install bash
```

Check the version:

```
bash --version
```

# Java

## SDKMAN

Can add a `.sdkmanrc` file to java repo

```
curl -s "https://get.sdkman.io" | bash
source ~/.sdkman/bin/sdkman-init.sh
sdk install java 21.0.3-tem
```

Then add this to `~/.sdkman/etc/config` so the `.sdkmanrc` auto-applies:

```
sdkman_auto_env=true
```


```
which java
```

Should output something like:

```
/Users/logan/.sdkman/candidates/java/current/bin/java
```

# Vim

mkdir -p ~/.vim/pack/plugins/start
clone the plugin you want, into that directory
    `git clone https://github.com/franbach/miramare.git ~/.vim/pack/plugins/start/miramare`
    `git clone https://github.com/franbach/miramare.git ~/.vim/pack/plugins/start/miramare`
    `git clone https://github.com/preservim/nerdtree.git ~/.vim/pack/plugins/start/nerdtree`
    `git clone https://github.com/vim-airline/vim-airline ~/.vim/pack/plugins/start/vim-airline`
    `git clone https://github.com/vim-airline/vim-airline-themes ~/.vim/pack/plugins/start/vim-airline-themes`
    `git clone https://github.com/fatih/vim-go.git ~/.vim/pack/plugins/start/vim-go`

# Neovim

[Installation Instructions](https://github.com/neovim/neovim/wiki/Installing-Neovim)

I installed via `brew install neovim`

My inital neovim configuration was copy and pasted from here: https://github.com/nvim-lua/kickstart.nvim/blob/master/init.lua

- mkdir -p ~/.config/nvim
- cd .config/nvim
- nvim init.lua
- Copy and paste kickstart.nvim into init.lua

- This config uses lazy.nvim for package management. To delete and reinstall everything follow the below steps and then reopen neovim:

To uninstall lazy.nvim and its associated package data, you need to remove the following files and directories:

    - data: ~/.local/share/nvim/lazy
    - state: ~/.local/state/nvim/lazy
    - lockfile: ~/.config/nvim/lazy-lock.json

- lazy.nvim - Pluigin manager
- Mason - Installers for LSP, Formatters, Linters, and etc.


When typing commands (:) start typing and hit <tab> to get auto sugestions


- Mason
    - installs packages to `~/.local/share/nvim/mason`
    - MasonInstall autopep8
    - MasonUninstall autopep8    
- nvim-tree (:h nvim-tree) Docs located [here](https://github.com/nvim-tree/nvim-tree.lua/blob/master/doc/nvim-tree-lua.txt#L1508)
    :NvimTreeToggle
    :NvimTreeCollapse




# VS Code

# Neofetch

`brew install neofetch`

# TODO

https://github.com/LunarVim/Neovim-from-scratch/blob/02-keymaps/lua/user/keymaps.lua

https://www.reddit.com/r/neovim/comments/1rhxmyz/show_off_your_neovim_with_a_screensaver_matrix/


## keybinds custom 

https://github.com/ray-x/nvim/blob/a1dbd320fd693a9c9c62041eb062dbe2a16ce939/lua/core/commands.lua#L113

## Null ls

https://www.josean.com/posts/neovim-linting-and-formatting

https://www.youtube.com/watch?v=i04sSQjd-qo 7:12

## Status Line

https://github.com/nvim-lualine/lualine.nvim

## Breadcrums

https://github.com/utilyre/barbecue.nvim

## Lsp saga

https://github.com/bibjaw99/workstation/blob/9481d31a20beffb7c24508b201b486f08aeea5d5/.config/nvim/lua/grimmvim/plugins/lsp/lspsaga.lua#L2

https://nvimdev.github.io/lspsaga/definition/

## Lua Snippets

https://github.com/L3MON4D3/LuaSnip

## Snacks

https://github.com/folke/snacks.nvim

indent

## Basile

https://github.com/davidbasilefilho/basile.nvim

## Zen Mode

https://github.com/davidbasilefilho/basile.nvim/blob/master/lua/custom/plugins/zen-mode.lua

## Avante

https://github.com/yetone/avante.nvim

## alpha

https://github.com/goolord/alpha-nvim/discussions/16#discussioncomment-1309233


NEOVIM Bloody https://patorjk.com/software/taag/#p=display&v=0&f=Bloody&t=NEOVIM




## tmux

https://www.youtube.com/watch?v=H70lULWJeig

https://www.youtube.com/watch?v=wNQpDWLs4To


`brew install tmux`

# Mole

macOS cleanup & system maintenance tool.

`brew install mole`

```
mo                           # Interactive menu
mo clean                     # Deep cleanup + already-uninstalled app leftovers
mo uninstall                 # Remove installed apps + their leftovers
mo optimize                  # Refresh caches & services
mo analyze                   # Visual disk explorer (or 'mo analyse')
mo status                    # Live system health dashboard
mo purge                     # Clean project build artifacts
mo installer                 # Find and remove installer files

mo touchid                   # Configure Touch ID for sudo
mo completion                # Set up shell tab completion
mo update                    # Update Mole
mo update --nightly          # Update to latest unreleased main build, script install only
mo remove                    # Remove Mole from system
mo --help                    # Show help
mo --version                 # Show installed version
```

Preview safely:

```
mo clean --dry-run
mo uninstall --dry-run
mo history
mo history --json
mo purge --dry-run

# Also works with: optimize, installer, remove, completion, touchid enable
mo clean --dry-run --debug   # Preview + detailed logs
mo optimize --whitelist      # Manage protected optimization rules
mo clean --whitelist         # Manage protected caches
mo purge --paths             # Configure project scan directories
mo analyze /Volumes          # Analyze external drives only
```

# LaTeX

Installed via `brew install --cask mactex` (TeX Live 2026). All tools live at `/Library/TeX/texbin/`, so no extra setup is needed.

This setup uses **latexmk** — that's what the Neovim vimtex config sets as the compiler (`vimtex_compiler_method = "latexmk"`), and the existing `resume.fdb_latexmk` confirms it's what last built the PDF. The file uses only standard packages, so the default **pdfLaTeX** engine is correct (no XeLaTeX/fontspec needed).

Compile from the command line:

```
latexmk -pdf resume.tex
```

That runs pdfLaTeX as many times as needed (resolves refs) and writes `resume.pdf`.

Inside Neovim (vimtex), open `resume.tex` and hit `\ll` to compile, `\lv` to view in Skim.

Clean up the aux junk (`.aux .log .out .fls .fdb_latexmk .synctex.gz`) when you're done:

```
latexmk -c resume.tex     # remove aux files, keep PDF
latexmk -C resume.tex     # also remove the PDF
```

# New Machine Setup

Steps to set up zsh, neovim, and wezterm on a fresh Mac.

## 1. Clone the repo

```
git clone <your-repo-url> ~/dotfiles
```

## 2. Install dependencies

```
brew install neovim jq tmux imagemagick eza zoxide bat asciiquarium lazygit fzf ranger ripgrep gh mole
brew install --cask wezterm mactex skim
brew install font-meslo-lg-nerd-font
```

## 3. Install Oh My Zsh + plugins

```
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Theme:
```
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

Plugins:
```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/fdellwing/zsh-bat.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-bat
```

zsh-autocomplete (installed separately, not as an oh-my-zsh plugin):
```
mkdir -p ~/zshrc-plugins
git clone https://github.com/marlonrichert/zsh-autocomplete.git ~/zshrc-plugins/zsh-autocomplete
```

Run `p10k configure` if the configuration wizard doesn't start automatically.

## 4. Install NVM, Pyenv, and Go (optional)

These are referenced in .zshrc. Install whichever you need:

```
# NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Pyenv (Python Version Manager)
brew install pyenv

# Go
brew install go
```

## 5. Create symlinks

```
ln -s ~/dotfiles/.zshrc ~/.zshrc
ln -s ~/dotfiles/.vimrc ~/.vimrc
mkdir -p ~/.config
ln -s ~/dotfiles/nvim ~/.config/nvim
ln -s ~/dotfiles/tmux/.tmux.conf ~/.tmux.conf
ln -s ~/dotfiles/wezterm-config/.wezterm.lua ~/.wezterm.lua
ln -s ~/dotfiles/vscode/keybindings.json ~/Library/Application\ Support/Code/User/keybindings.json
ln -s ~/dotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json
mkdir -p ~/.claude
ln -s ~/dotfiles/claude/settings.json ~/.claude/settings.json
ln -s ~/dotfiles/claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -s ~/dotfiles/claude/skills ~/.claude/skills
ln -s ~/dotfiles/claude/agents ~/.claude/agents
ln -s ~/dotfiles/opencode/opencode.json ~/.config/opencode/opencode.json
```

## 6. Open Neovim

Just run `nvim` — lazy.nvim will auto-install all plugins on first launch. Then run `:Mason` to install any LSP servers/formatters you need.

## 7. Set up GitHub CLI (gh)

`gh` is installed via brew in step 2. Authenticate it so Claude Code has access to Github:

```
gh auth login
```

Follow the prompts:
- Select `GitHub.com`
- Choose `HTTPS` or `SSH` as your preferred protocol
- Authenticate via web browser (easiest) or paste a personal access token

Verify the login:

```
gh auth status
```

## 8. Verify setup

Run the setup check script to confirm all packages are installed and symlinks are correct:

```
chmod +x ~/dotfiles/setup.sh
./setup.sh
```
