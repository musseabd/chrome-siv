#!/bin/bash

print_usage() {
	echo "$0 <dut_ip> <port_num> <device>"
	echo "port_num is one of {0, 1}"
	echo "device is one of {USB, TBT3, TBT4_USB4, DP_CABLE, DP_DOCK}"
	echo "Usage example: $0 10.165.176.63 1 DP_DOCK"
}

TEMP=$(getopt -o h --long help:: -- "$@")
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

echo "$0 $dutip $port $device"


# TODO: validate dutip and other input arguments
# validate dutip isn't empty string
if [ -z "$dutip" ]; then  print_usage; fi

# validate outfilepath isn't empty string
if [ -z "$outfilepath" ]; then  outfilepath="dut_log.txt"; fi

# TODO: handle "host public key is unknown" and "IP public key changed"
# TODO: may be use public key authentication instead of sshpass
SSH_HOST_KEY_OPT="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"


dut_log_dir="/usr/local/tcss_debug_util/"
collect_log_file_name="tcss_collect_logs_dut.sh"

# 1. copy dut_collect_logs.sh to dut
# create dir on dut
eval sshpass -p "test0000" ssh $SSH_HOST_KEY_OPT root@$dutip 'rm -rf $dut_log_dir'
eval sshpass -p "test0000" ssh $SSH_HOST_KEY_OPT root@$dutip 'mkdir $dut_log_dir'
# copy log collecting script to dut
eval sshpass -p "test0000" scp $SSH_HOST_KEY_OPT ./tcss_collect_logs_dut.sh root@$dutip:$dut_log_dir

# 2. run log collecting script on dut
sshpass -p "test0000" ssh $SSH_HOST_KEY_OPT root@$dutip "cd $dut_log_dir && chmod +x $collect_log_file_name && ./$collect_log_file_name "$port $device""

# 3. copy output back to host
log_file_name="dut_log.txt"
dut_log_file_path=$dut_log_dir/$log_file_name
sshpass -p "test0000" scp $SSH_HOST_KEY_OPT root@$dutip:$dut_log_file_path  $outfilepath

