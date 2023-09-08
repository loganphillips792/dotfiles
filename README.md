# dotfiles

These are the dofiles I use on Mac OS.

# Zshell Set up

If you keep your zshrc somewhere other than your home directory (~), then you wil have to use a symlink. For example, I store my dot files in ~/dotfiles.

- ln -s ~/dotfiles/.zshrc ~/.zshrc

When you restart your terminal, you should see your Zshr configured properly

## Oh My ZSH

[Repo Link](https://github.com/ohmyzsh/ohmyzsh/)

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    Installs at ~/.oh-my-zsh
    ls ~/.oh-my-zsh
    
    themes located at .oh-my-zsh/themes
    Any plugins you want to use, add to the plugins=() variable

    I am currently using powerlevel10k theme. View the installation instructions [here](https://github.com/romkatv/powerlevel10k#oh-my-zsh). I followed the instructions for 'Oh My ZSH'. It will take you through a wizard in order to configure the theme. Ultimtately installs the configuration at ~/.pk10.zsh. Note, this also uses the "Meslo Nerd Font". View the repo to install this font.