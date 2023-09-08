# dotfiles

These are the dofiles I use on Mac OS.

ln -s ~/dotfiles/.zshrc ~/.zshrc
ln -s ~/dotfiles/.vimrc ~/.vimrc

# Zshell Set up

If you keep your zshrc somewhere other than your home directory (~), then you wil have to use a symlink. For example, I store my dot files in ~/dotfiles.

When you restart your terminal, you should see your Zshr configured properly


## Oh My ZSH

[Repo Link](https://github.com/ohmyzsh/ohmyzsh/)

sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    Installs at ~/.oh-my-zsh
    ls ~/.oh-my-zsh
    
    themes located at .oh-my-zsh/themes
    Any plugins from oh-my-zsh you want to use, add to the plugins=() variable

    I am currently using powerlevel10k theme. View the installation instructions [here](https://github.com/romkatv/powerlevel10k#oh-my-zsh). I followed the instructions for 'Oh My ZSH'. It will take you through the "configuration wizard" in order to configure the theme. Ultimtately installs the configuration at ~/.pk10.zsh. Note, this also uses the "Meslo Nerd Font". View the repo to install this font.


# Vim

mkdir -p ~/.vim/pack/plugins/start
clone the plugin you want, into that directory
    git clone https://github.com/franbach/miramare.git ~/.vim/pack/plugins/start/miramare
    git clone https://github.com/franbach/miramare.git ~/.vim/pack/plugins/start/miramare
    git clone https://github.com/preservim/nerdtree.git ~/.vim/pack/plugins/start/nerdtree
    git clone https://github.com/vim-airline/vim-airline ~/.vim/pack/plugins/start/vim-airline
    git clone https://github.com/vim-airline/vim-airline-themes ~/.vim/pack/plugins/start/vim-airline-themes
    git clone https://github.com/fatih/vim-go.git ~/.vim/pack/plugins/start/vim-go


