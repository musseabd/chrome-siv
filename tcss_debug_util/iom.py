import logging

import dut_log
import typec_devices
import tcss_util


IOM_STATUS_NAME__PORT_IS_CONNECTED = PORT_CONNECTED = "[31]PORT_IS_CONNECTED"
IOM_STATUS_BIT_START__PORT_IS_CONNECTED = 31
IOM_STATUS_MASK__PORT_IS_CONNECTED  = 1 << IOM_STATUS_BIT_START__PORT_IS_CONNECTED

IOM_STATUS_NAME__ACTIVITY_TYPE = ACTIVITY_TYPE = "[9:6]ACTIVITY_TYPE"
IOM_STATUS_BIT_START__ACTIVITY_TYPE = 6
IOM_STATUS_MASK__ACTIVITY_TYPE  = 0xF << IOM_STATUS_BIT_START__ACTIVITY_TYPE

IOM_STATUS_NAME__CONFIG_DONE = CONFIG_DONE = "[5]CONFIG_DONE"
IOM_STATUS_BIT_START__CONFIG_DONE = 5
IOM_STATUS_MASK__CONFIG_DONE  = 1 << IOM_STATUS_BIT_START__CONFIG_DONE


IOM_STATUS_NAME__PORT_IN_TRANSITION = PORT_IN_TRANSITION = "[4]PORT_IN_TRANSITION"
IOM_STATUS_BIT_START__PORT_IN_TRANSITION = 4
IOM_STATUS_MASK__PORT_IN_TRANSITION  = 1 << IOM_STATUS_BIT_START__PORT_IN_TRANSITION

IOM_STATUS_NAME__PORT_EN = PORT_EN = "[3]PORT_EN"
IOM_STATUS_BIT_START__PORT_EN = 3
IOM_STATUS_MASK__PORT_EN  = 1 << IOM_STATUS_BIT_START__PORT_EN


ACTIVITY_TYPE__USB3 = 0x3
ACTIVITY_TYPE__ALT_MODE_DP = 0x5
ACTIVITY_TYPE__ALT_MODE_DP_MFD = 0x6
ACTIVITY_TYPE__ALT_MODE_TBT = 0x7
ACTIVITY_TYPE__ALT_MODE_USB3 = 0xc
ACTIVITY_TYPE__ALT_MODE_TBT_USB3 = 0xd



expected_iom_port_status = {
	typec_devices.DP_DOCK : 	{PORT_EN: 0x1, PORT_CONNECTED: 0x1, CONFIG_DONE: 0x1, PORT_IN_TRANSITION: 0x0, ACTIVITY_TYPE: ACTIVITY_TYPE__ALT_MODE_DP_MFD},
	typec_devices.DP_CABLE : 	{PORT_EN: 0x1, PORT_CONNECTED: 0x1, CONFIG_DONE: 0x1, PORT_IN_TRANSITION: 0x0, ACTIVITY_TYPE: ACTIVITY_TYPE__ALT_MODE_DP},
	typec_devices.TBT3: 		{PORT_EN: 0x1, PORT_CONNECTED: 0x1, CONFIG_DONE: 0x1, PORT_IN_TRANSITION: 0x0, ACTIVITY_TYPE: ACTIVITY_TYPE__ALT_MODE_TBT},
	typec_devices.TBT4_USB4 : 	{PORT_EN: 0x1, PORT_CONNECTED: 0x1, CONFIG_DONE: 0x1, PORT_IN_TRANSITION: 0x0, ACTIVITY_TYPE: ACTIVITY_TYPE__ALT_MODE_TBT_USB3},
	typec_devices.USB : 		{PORT_EN: 0x1, PORT_CONNECTED: 0x1, CONFIG_DONE: 0x1, PORT_IN_TRANSITION: 0x0, ACTIVITY_TYPE: ACTIVITY_TYPE__USB3}
}


def val_to_str_iom_port_status(key_str, val):
	return hex(val)
	

def iom_check_status(port, connected_device, monitor_plugged):
	dut_iom_status = dut_log.get_iom_status_register_from_log(port)

	dut_iom_satus_port_connected = (dut_iom_status & IOM_STATUS_MASK__PORT_IS_CONNECTED) >> IOM_STATUS_BIT_START__PORT_IS_CONNECTED
	dut_iom_satus_config_done = (dut_iom_status & IOM_STATUS_MASK__CONFIG_DONE) >> IOM_STATUS_BIT_START__CONFIG_DONE
	dut_iom_satus_port_in_trans = (dut_iom_status & IOM_STATUS_MASK__PORT_IN_TRANSITION) >> IOM_STATUS_BIT_START__PORT_IN_TRANSITION
	dut_iom_satus_port_activity_type = (dut_iom_status & IOM_STATUS_MASK__ACTIVITY_TYPE) >> IOM_STATUS_BIT_START__ACTIVITY_TYPE
	dut_iom_satus_port_en = (dut_iom_status & IOM_STATUS_MASK__PORT_EN) >> IOM_STATUS_BIT_START__PORT_EN


	iom_status_actual = {
		PORT_CONNECTED: dut_iom_satus_port_connected,
		CONFIG_DONE: dut_iom_satus_config_done,
		PORT_IN_TRANSITION: dut_iom_satus_port_in_trans,
		ACTIVITY_TYPE: dut_iom_satus_port_activity_type,
		PORT_EN: dut_iom_satus_port_en
	}

	iom_status_expected = expected_iom_port_status[connected_device]

	tcss_util.print_actual_vs_expected("Check iom port status register", iom_status_expected, iom_status_actual, val_to_str_iom_port_status, attr_width=16)

	# print activity type to help user decode bits
	print("Activity Type: 0x0: Undefined, 0x3: USB3, 0x5: Alt mode DP, 0x6: Alt mode DP MFD,  0x7: Alt mode TBT, 0xC: Alt mode USB3 0xD: Alt mode TBT USB3 0xE: No TBT allowed")