# Hacks
Contains general code/scripts that come handy for linux developers

## dotfiles
Contains dotfiles , currently just for tmux and vim . configures with powerline.
`Usage : ./init.sh`
`to undo changes : ./init.sh -r `
Currently tested on Fedora 27 and Ubuntu 17.10

## lsmod2config
Converts a given lsmod output to a set of linux `CONFIG_*` options
(Found that linux kernel build has opton LSMOD which does the same)

## rpmbuild\_docker
[Still under development]
A Docker setup that can build kernel rpms for RHEL-like distros.

## get most contacted (LINUX + ANDROID ONLY) 
A script that can extract data from you phone and tell you whom have you
contacted the most, this data is being tracked as part of google contacts
Every whatsapp/call/text increments `contacted_times`.

Script uses this information to tell you whom you contacted the most
with the phone which has your google login.
