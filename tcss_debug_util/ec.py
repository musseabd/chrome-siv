import logging

import dut_log
import typec_devices
import tcss_util

# ? will be filled depending on whether display is connected or not
expected_mux_info = {
	typec_devices.DP_DOCK : 	{"USB": "1", "DP": "1", "HPD_IRQ": "0", "HPD_LVL": "?", "SAFE": "0", "TBT": "0", "USB4": "0"},
	typec_devices.DP_CABLE : 	{"USB": "0", "DP": "1", "HPD_IRQ": "0", "HPD_LVL": "?", "SAFE": "0", "TBT": "0", "USB4": "0"},
	typec_devices.TBT3: 		{"USB": "0", "DP": "0", "HPD_IRQ": "0", "HPD_LVL": "0", "SAFE": "0", "TBT": "1", "USB4": "0"},
	typec_devices.TBT4_USB4 : 	{"USB": "0", "DP": "0", "HPD_IRQ": "0", "HPD_LVL": "0", "SAFE": "0", "TBT": "0", "USB4": "1"},
	typec_devices.USB : 		{"USB": "1", "DP": "0", "HPD_IRQ": "0", "HPD_LVL": "0", "SAFE": "0", "TBT": "0", "USB4": "0"}
}

def ec_get_expected_mux_settings(port, connected_device, monitor_plugged):
	expected = expected_mux_info[connected_device].copy()

	# adjust HPD_LVL signal based on whether DP display is on or not
	if connected_device == typec_devices.DP_DOCK or connected_device == typec_devices.DP_CABLE:
		expected["HPD_LVL"] = "1" if monitor_plugged else "0"

	return expected


def ec_check_mux(port, connected_device, monitor_plugged=False):

	test_pass = True

	actual_mux_settings = dut_log.dut_log_get_pdmuxinfo(port)


	logging.debug("expected", actual_mux_settings)

	# get the right expected settings file for the connection
	expected_mux_settings = ec_get_expected_mux_settings(port, connected_device, monitor_plugged)


	tcss_util.print_actual_vs_expected("Check ec mux info", expected_mux_settings, actual_mux_settings)



