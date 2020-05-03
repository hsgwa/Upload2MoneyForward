#!/bin/bash
# usage sjis_to_utf8.sh download

cd `dirname $0`
csvs=(`find $1 -name "*.csv" | sort -h | xargs`)
for csv in ${csvs[@]}; do
	type=`nkf --guess $csv`
	if [[ $type = *"Shift_JIS"* ]] ; then
		nkf -w --overwrite $csv
	fi
done
