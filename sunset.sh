#!/bin/bash
# Build and Install 'redshift' for wayland: https://github.com/minus7/redshift
# You can also use gammastep

#cd $HOME/.local/bin
# killing gammastep if it already exists
if [[ $(pgrep gammastep) =~ ^[0-9]+$ ]]
	then
		kill $(pgrep gammastep)

	else
		gammastep -PO 3200
fi

