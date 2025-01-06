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

- Any plugins from oh-my-zsh you want to use, add to the plugins=() variable
- Zshell plugins: I created a folder `~/zshrc-plugins` and this is where I `git clone` plugins into.
- I am currently using powerlevel10k theme. View the installation instructions [here](https://github.com/romkatv/powerlevel10k#oh-my-zsh). I followed the instructions for 'Oh My ZSH'. It will take you through the "configuration wizard" in order to configure the theme. Ultimtately installs the configuration at ~/.pk10.zsh. Note, this also uses the "Meslo Nerd Font". View the repo to install this font.

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

## keybinds custom 

https://github.com/ray-x/nvim/blob/a1dbd320fd693a9c9c62041eb062dbe2a16ce939/lua/core/commands.lua#L113



## Null ls

https://www.josean.com/posts/neovim-linting-and-formatting

https://www.youtube.com/watch?v=i04sSQjd-qo 7:12

## Wez term config

https://github.com/KevinSilvester/wezterm-config?tab=readme-ov-file
