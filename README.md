# Hacks
Contains general code/scripts that come handy for linux developers

## lsmod2config
Converts a given lsmod output to a set of linux `CONFIG_*` options
Prerequisite : linux kernel source.

`./lsmod2config <linux_kernel_source> <lsmod_output>`

`Example : ./lsmod2config ~/linux lsmod `
