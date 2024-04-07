#!/bin/bash

print_usage() {
	echo "$0 <port_num> <device>"
	echo "port_num is one of {0, 1}"
	echo "device is one of {USB, TBT3, TBT4_USB4, DP_CABLE, DP_DOCK}"
	echo "Usage example: $0 1 DP_DOCK"
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

port=$1
device=$2

log_file="dut_log.txt"
touch $log_file
# clear log to start from scratch
echo > $log_file


run_cmd() {
	cmd_separator="========================================"
	
	# print separatorl
	echo $cmd_separator | tee -a $log_file
	
	cmd=$1
	
	echo $cmd | tee -a $log_file # print cmd in the log file
	eval "$cmd 2>&1 | tee -a $log_file" # execute cmd and append to to log file
	
	# print separator
	echo $cmd_separator | tee -a $log_file
}

# EC commands
# ec terminal
run_cmd "cat /var/log/cros_ec.log" # seems to not be uptodate log from ec. may be the ec logs here are from reboot time only

# Type C connection info
run_cmd "ectool version"
run_cmd "ectool  typecstatus $port"
run_cmd "ectool  usbpdmuxinfo"
run_cmd "ectool typecdiscovery $port 0" # SOP
run_cmd "ectool typecdiscovery $port 1" # SOP'
run_cmd "ectool gpioget"


## power delivery details
run_cmd "ectool usbpd $port"
run_cmd "ectool usbpdpower $port"
run_cmd "ectool infopddev $port"


# Kernel
## typecd deamon log
run_cmd "cat /var/log/typecd.log | grep -ai entered | grep 'mode on port $port'"

## device enumeration
run_cmd "lspci -k"
run_cmd "lsusb -t"
run_cmd "dmesg | grep thunderbolt"
run_cmd "dmesg | grep xhci"
run_cmd "ls /sys/bus/thunderbolt/devices"

## low power state for host controller and devices
run_cmd "cat /sys/bus/pci/devices/0000\:00\:0d.0/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:0d.2/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:0d.3/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:07.0/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:07.1/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:07.2/power/runtime_status"
run_cmd "cat /sys/bus/pci/devices/0000\:00\:07.3/power/runtime_status"
run_cmd "cat /sys/kernel/debug/dri/0/i915_dmc_info"

# display
run_cmd "intel_reg read c40000 c4004 c4008 c400c c4030 c4034 16f270 16f470 16f670 16f870 16fe50 16fe54 16fe58 165e5c 161500"
run_cmd "dmesg | grep -i training"
run_cmd "dmesg | grep -i vbt"



screebo_port_to_soc_port() {
	port=$1
	

	if [[ port -eq 0 ]]; then
		echo 1
	elif [[ port -eq 1 ]]; then
		echo 3
	else
		echo "Error "
		echo "\tunsupported port"
		exit 1
	fi
}

# iom
board_port_to_soc_port() {
	board=$1
	port=$2

	case "$board" in
		"screebo")
			echo $(screebo_port_to_soc_port $port)			
			;;
		*)
			echo "Error "
			echo "\tadd board to board_port_to_soc_port"
			exit 1
			;;
	esac

}
board="screebo"
soc_port=$(board_port_to_soc_port $board $port)
port_status_addrs=$(printf "0x%x" $((0x3fff0aa0160 + 4*$soc_port)))
run_cmd "iotools mmio_read32 $port_status_addrs" # (port-0 [base + offset = 0x000003FFF0AA0000 + 0x160])
