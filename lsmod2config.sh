#!/bin/bash

# expects LINUX_DIR 

if [ $# -ne 2 ] ; then
	echo "Usage :"
	echo "$0 <linux_kernel_source> <lsmod_output>"
	exit
fi

if [ ! -d $1 ] ; then
	echo "$1 directory does not exits"
	exit
fi

if [ ! -f $2 ] ; then
	echo "$2  does not exits"
	exit
fi
for modules in `cat $2 | awk '{print $1}'`
do
	str="\b$modules\.o\b"
	line=`grep -R --include=Makefile  $str  $1`
	echo $line | awk -F"[()]" '{print $2}'i 
done
