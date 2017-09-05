#!/bin/bash

LINUX_DIR=/path/to/kernel/source/

for modules in `cat lsmod | awk '{print $1}'`
do
	str="\b$modules\.o\b"
	line=`grep -R --include=Makefile  $str  $LINUX_DIR`
	echo $line | awk -F"[()]" '{print $2}'i 
done
