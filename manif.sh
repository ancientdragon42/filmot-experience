#!/bin/bash

process() {
    cd $1
    if [ -f .source ]; then
	for src in `cat .source`; do
	    ../extract.py $src &
	done
    fi
}

for item in `ls`; do
    if [ -d $item ]; then process $item & fi
done
process '.'
