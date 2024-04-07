import typec_devices
import kernel_thunderbolt
import dut_log
import tcss_util

def kernel_check_typecd(port, connected_device):
	title = "check typecd log"

	cmd_output = dut_log.get_typecd_enetered_mode(port)

	if connected_device == typec_devices.TBT4_USB4:
		tcss_util.print_result_string_in_cmd_output(title, f"Entered USB4 mode on port {port}", cmd_output)
	elif connected_device in (typec_devices.DP_CABLE, typec_devices.DP_DOCK):
		tcss_util.print_result_string_in_cmd_output(title, f"Entered DP mode on port {port}", cmd_output)
	

def kernel_check_lspci():

	cmd_output = dut_log.get_lspci("00:0d.0")
	tcss_util.print_result_all_strings_in_cmd_output("check usb3 pci device is enumerated",
											  ["Kernel driver in use: xhci_hcd"], cmd_output)

	cmd_output = dut_log.get_lspci("00:0d.2")
	tcss_util.print_result_all_strings_in_cmd_output("check thunderbolt pci device 1 is enumerated",
											  ["Kernel driver in use: thunderbolt"], cmd_output)
	
	cmd_output = dut_log.get_lspci("00:0d.3")
	tcss_util.print_result_all_strings_in_cmd_output("check usb3 pci device 2 is enumerated",
											  ["Kernel driver in use: thunderbolt"], cmd_output)


def kernel_check_pci_runtime_status():

	expected_runtime_status = {
		"00:0d.0" : "active",
		"00:0d.2" : "active",
		"00:0d.3" : "active",
		"00:07.0" : "active",
		"00:07.2" : "active",
	}

	actual_runtime_status = {
		"00:0d.0" : dut_log.get_runtime_status("00:0d.0"),
		"00:0d.2" : dut_log.get_runtime_status("00:0d.2"),
		"00:0d.3" : dut_log.get_runtime_status("00:0d.3"),
		"00:07.0" : dut_log.get_runtime_status("00:07.0"),
		"00:07.2" : dut_log.get_runtime_status("00:07.2"),
	}

	tcss_util.print_actual_vs_expected("Check pci device power status", expected_runtime_status, actual_runtime_status, attr_width=16)


def kernel_check_i915_dmc_info():
	
	cmd_output = dut_log.get_command_output("cat /sys/kernel/debug/dri/0/i915_dmc_info", include_cmd=True)

	tcss_util.print_result_string_in_cmd_output("check if i915 is initialized", "DMC initialized: yes", cmd_output)


def kernel_check(port, connected_device, monitor_plugged=False):
	
	# if connected_device in (typec_devices.TBT3, typec_devices.TBT4_USB4):
	# 	kernel_thunderbolt.check_typecd_log(port)

	kernel_check_typecd(port, connected_device)

	kernel_check_lspci()

	kernel_check_pci_runtime_status()

	kernel_check_i915_dmc_info()

