import json
import logging

log_file_cmd_start_indicator = "========================================"

_log_file_path=""
def set_log_file_path(log_file_path):
	global _log_file_path
	_log_file_path = log_file_path

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


def get_command_output(cmd, include_cmd=False):
	cmd_output = ""
	found_cmd_start = False
	found_cmd_end = False

	with open(_log_file_path, 'r') as log_file:
		
		# find start of cmd
		while True:
			line = log_file.readline()

			if line == "": # end of file
				break
			
			cur_line = line.strip()
			next_line = peek_line(log_file).strip()

			if cur_line == log_file_cmd_start_indicator:
				# print(next_line)
				if next_line == cmd:
					cmd = log_file.readline().strip()
					found_cmd_start = True
					break

		if found_cmd_start:
			# at this point we have read the line with the command string
			# anything after this upto the next separator line is the command output
			while True:
				line = log_file.readline()

				if line == "": # end of file
					break
				
				cur_line = line.strip()
				
				if cur_line == log_file_cmd_start_indicator:
					# found the end, anything in between is the output
					found_cmd_end = True
					break
				
				cmd_output += line # add non-striped version to output string.

	if not found_cmd_start or not found_cmd_end:
		raise Exception(f"cmd {cmd}, cmd_start={found_cmd_start}, cmd_end={found_cmd_end}")

	if include_cmd:		
		cmd_output = cmd + "\n" + cmd_output

	return cmd_output.strip()
	

def dut_log_get_pdmuxinfo(port):

	# 1. get pd mux info command output
	cmd_output = get_command_output("ectool usbpdmuxinfo")

	if cmd_output.isspace():
		logging.error("empty cmd_ooutput")
		return


	# 2. parse pdmuxinfo output str and return a dictionary
	cmd_output = cmd_output.split('\n')

	port_0_str = cmd_output[0]
	port_1_str = cmd_output[1]

	# for the required port grab text after ":" and split by space
	port_str = port_0_str if port == 0 else port_1_str
	port_key_value_str_array = port_str.split(':')[1].split()
	

	# save each of property=value pair in dictionary
	mux_info_dict = {}
	for key_val_str in port_key_value_str_array:
		key_val = key_val_str.split("=")
		mux_info_dict[key_val[0]] = key_val[1]

	return mux_info_dict


type_c_board_port_to_soc_port_mapping = {
	"rex" : [0, 1],
	"screebo" : [1, 3] # 0 to 1, 1 to 3
}



def get_iom_status_register_from_log(port):
	# example: 
	# ========================================                                                         
	# iotools mmio_read32 0x3fff0aa0160    # this is for port 0                                                            
	# 0x804019a8                                                                                       
	# ========================================

	soc_port = type_c_board_port_to_soc_port_mapping["screebo"][port]

	port_status_address = 0x3fff0aa0160 + 4*soc_port
	cmd = f"iotools mmio_read32 {hex(port_status_address)}"

	print(f"{cmd}  {hex(port_status_address)}")

	iom_status = get_command_output(cmd).strip()
	return int(iom_status, 16)

def get_typecd_enetered_mode(port):

	cmd = f"cat /var/log/typecd.log | grep -ai entered | grep 'mode on port {port}'"

	cmd_output = get_command_output(cmd, include_cmd=True)

	# pick last line. i.e. the latest log
	# cmd_output = cmd_output.split('\n')
	# cmd_output = cmd_output[-1]

	return cmd_output

	
def get_lspci(pci_device_id_str):

	cmd = "lspci -k"
	device_info = ""

	cmd_output = get_command_output(cmd)

	lines = cmd_output.splitlines()

	for i in range(len(lines)):
		if pci_device_id_str in lines[i]:
			device_info += lines[i]
			device_info += lines[i+1]
			device_info += lines[i+2]

	return device_info


def get_runtime_status(pci_dev):
	pci_bus = pci_dev.split(":")[0]
	
	cmd = f"cat /sys/bus/pci/devices/0000\:{pci_bus}\:0d.0/power/runtime_status"

	return get_command_output(cmd)




