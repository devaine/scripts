#!/bin/bash


## Variables
declare -r time=$(date --iso-8601=seconds)


while(( $# > 0)); do
	case $1 in
	   -s)
		REGION=yes
		shift
		;;
	   -c)
		CURSOR=yes
		shift
		;;
	   *)
		if [ -z "$FILENAME" ]; then
		   FILENAME="$1/$time.png"
		   shift
		else
		   echo "wrong format"
		   exit 1
		fi
		;;
esac
done

OPTS=()
if [ -n "$REGION" ]; then
	OPTS+=("-g $(slurp)")

	if [ -n "$CURSOR" ]; then
		OPTS+=("-c")
	fi
fi

grim "${OPTS[@]}" "$FILENAME"
# https://github.com/bugaevc/wl-clipboard/issues/198 lifesaver
wl-copy --type image/png < $FILENAME 
