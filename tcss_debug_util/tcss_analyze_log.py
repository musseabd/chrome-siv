#!/bin/python

import sys
import argparse

import dut_log
import ec
import iom
import kernel
import typec_devices

# parse arguments
parser = argparse.ArgumentParser(description="analyze TCSS log")
parser.add_argument('port', type=int, choices=[0,1], help="port number")
parser.add_argument('device', choices=["USB", "TBT3", "TBT4_USB4", "DP_CABLE", "DP_DOCK"], help="connected device string")
parser.add_argument('--monitor_plugged', action="store_true", default=False, help="indicates an external display is connected (either directly or thru dock) and turned on")
parser.add_argument('--log_file', default='./dut_log.txt', help="path of log file")
args = parser.parse_args()

log_file = args.log_file
port = args.port
device = args.device
monitor_plugged = args.monitor_plugged



dut_log.set_log_file_path(args.log_file)

ec.ec_check_mux(port=port, connected_device=device, monitor_plugged=monitor_plugged)

iom.iom_check_status(port=port, connected_device=device, monitor_plugged=monitor_plugged)

kernel.kernel_check(port=port, connected_device=device, monitor_plugged=monitor_plugged)

