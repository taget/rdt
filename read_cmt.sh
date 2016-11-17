#!/bin/bash

function error_out {
    echo "error" $1
    exit 1
}

function get_cmt {
	local cmt_b=$(sudo virsh domstats $1 | tail -3 | awk -F= '{print $2}' | head -1)

	# turn to KB 8 * 1024 = 8192 
	local cmt_K=$((cmt_b / 8192 ))
	local cmt_M=$((cmt_B / 1024 ))
        echo $cmt_K
#	echo $cmt_K "KB"
#	echo $cmt_M "MB"

}

if [[ -z $1 ]]; then
    error_out "No dom specify!"
fi

DOM_COUNT=$#
LLC_USED=0

echo "Cache Usage:"
for dom in "$@"; do
	llc=$(get_cmt $1)
        echo "$1 : $llc K"
        LLC_USED=$((LLC_USED + llc))
	shift
done

echo "-----  -----------"
echo "Count: "$DOM_COUNT

echo "TOTAL: "$LLC_USED K
echo "AVG: "$(( LLC_USED / DOM_COUNT )) K

