#!/bin/bash
PKG_MGR=""

set -x

if [ "$1" == "-r" ]
then
	APT_ACTION="remove"
	PIP_ACTION="uninstall"
else
	APT_ACTION="install"
	PIP_ACTION="install"
fi

#Detect package manager
apt -h > /dev/null 2>/dev/null
if [ $? -eq 0 ]; then
	PKG_MGR=apt
fi
yum -h > /dev/null 2>/dev/null
if [ $? -eq 0 ] ; then
	PKG_MGR=yum
	dnf -h >/dev/null 2>/dev/null
	if [ $? -eq 0 ] ; then
		PKG_MGR=dnf
	fi
else
	apt -h > /dev/null 2>/dev/null
	if [ $? -eq 0 ]; then
		PKG_MGR=apt
	fi
fi
echo $PKG_MGR

#install vim and tmux
sudo test 1 == 1 > /dev/null
if [ $? -ne 0 ] ; then
	echo "User is not a sudoer"
fi
sudo $PKG_MGR $APT_ACTION tmux vim python-pip git -y
sudo su -c " pip $PIP_ACTION git+git://github.com/Lokaltog/powerline"


if [ $APT_ACTION == install ]
then
	# get powerline fonts in place
	wget https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
	wget https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
	sudo mv PowerlineSymbols.otf /usr/share/fonts/
	sudo mv 10-powerline-symbols.conf /etc/fonts/conf.d/
	sudo fc-cache -vf
	#install vundle
	git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
	#install tpm
	git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
	#find python powerline package location
	POWERLINE_PATH=`pip show  powerline-status |grep Location: | cut -d " " -f2`
	sed  -e "s!PPTH!$POWERLINE_PATH\/powerline/bindings!" tmux.conf1 | tee tmux.conf
	#put tmux conf inplace
	ln -sf $PWD/tmux.conf $HOME/.tmux.conf
	#put vim rc inplace
	ln -sf $PWD/vimrc $HOME/.vimrc
	#install all vim plugins
	vim +PluginInstall +qall
else
	rm -rf ~/.vim/bundle  ~/.tmux/plugins/tpm
	rm /usr/share/fonts/PowerlineSymbols.otf
	rm /etc/fonts/conf.d/10-powerline-symbols.conf
	unlink $HOME/.tmux.conf
	unlink $HOME/.vimrc
fi
