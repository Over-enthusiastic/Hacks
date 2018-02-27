#!/bin/bash


set -x
internal="LVDS-1"
extern="HDMI-1"

if xrandr |grep "$extern disconnected" ; then
	xrandr --output "$extern" --off --output "$internal" --auto
else
	xrandr --output "$internal" --off --output "$extern" --auto
fi

