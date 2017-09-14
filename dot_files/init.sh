#!/bin/bash
PKG_MGR=""

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
sudo $PKG_MGR install tmux vim tmux-powerline -y
