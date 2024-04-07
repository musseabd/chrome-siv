#!/bin/bash

print_usage() {
	echo "$0 <dut ip> <port num> <device>"
	echo "device is one of {USB , TBT3 , TBT4_USB4 , DP_CABLE , DP_DOCK}"
	echo "Usage example: $0 10.165.176.63 1 DP_DOCK"
}

set -e # exit on first error

source ./tcss_util.sh

# get inputs from command line

TEMP=$(getopt -o h --long help,monitor_plugged:: -- "$@")
if [[ $? -ne 0 ]]; then
	print_usage
	exit 1;
fi

eval set -- "$TEMP"

while true ; do
	case "$1" in
		--help|-h)
			print_usage
			exit 0
			;;
		--monitor_plugged)
			monitor_plugged="--monitor_plugged"
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			echo "Error "
			print_usage
			exit 1
			;;
	esac
done


dutip=$1
port=$2
device=$3

echo $dutip
echo $port
echo $device
echo $monitor_plugged

validatie_device $device

#if [ ! -z "$display_on" ]; then  display_on="--display_on"; fi

./tcss_get_log_from_dut.sh $dutip $port $device
./tcss_analyze_log.py $port $device $monitor_plugged
