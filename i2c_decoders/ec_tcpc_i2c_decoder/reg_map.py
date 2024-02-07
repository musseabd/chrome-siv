REG_MAP_ADDR = "addr"
REG_MAP_NAME = "name"
REG_MAP_SIZE = "size"

reg_map = {
    
        "0x00" : {
                REG_MAP_NAME : "VENDOR_ID ",
                REG_MAP_SIZE : 2
        },

        "0x02" : {
                REG_MAP_NAME : "PRODUCT_ID ",
                REG_MAP_SIZE : 2
        },

        "0x04" : {
                REG_MAP_NAME : "DEVICE_ID ",
                REG_MAP_SIZE : 2
        },

        "0x06" : {
                REG_MAP_NAME : "USBTYPEC_REV ",
                REG_MAP_SIZE : 2
        },

        "0x08" : {
                REG_MAP_NAME : "USBPD_REV_VER ",
                REG_MAP_SIZE : 2
        },

        "0x0A" : {
                REG_MAP_NAME : "PD_INTERFACE_REV ",
                REG_MAP_SIZE : 2
        },

        "0x10" : {
                REG_MAP_NAME : "ALERT ",
                REG_MAP_SIZE : 2
        },

        "0x12" : {
                REG_MAP_NAME : "ALERT_MASK ",
                REG_MAP_SIZE : 2
        },

        "0x14" : {
                REG_MAP_NAME : "POWER_STATUS_MASK ",
                REG_MAP_SIZE : 1
        },

        "0x15" : {
                REG_MAP_NAME : "FAULT_STATUS_MASK ",
                REG_MAP_SIZE : 1
        },

        "0x16" : {
                REG_MAP_NAME : "EXTENDED_STATUS _MASK",
                REG_MAP_SIZE : 1
        },

        "0x17" : {
                REG_MAP_NAME : "ALERT_EXTENDED _MASK",
                REG_MAP_SIZE : 1
        },

        "0x18" : {
                REG_MAP_NAME : "CONFIG_STANDARD _OUTPUT",
                REG_MAP_SIZE : 1
        },

        "0x19" : {
                REG_MAP_NAME : "TCPC_CONTROL ",
                REG_MAP_SIZE : 1
        },

        "0x1A" : {
                REG_MAP_NAME : "ROLE_CONTROL ",
                REG_MAP_SIZE : 1
        },

        "0x1B" : {
                REG_MAP_NAME : "FAULT_CONTROL ",
                REG_MAP_SIZE : 1
        },

        "0x1C" : {
                REG_MAP_NAME : "POWER_CONTROL ",
                REG_MAP_SIZE : 1
        },

        "0x1D" : {
                REG_MAP_NAME : "CC_STATUS ",
                REG_MAP_SIZE : 1
        },

        "0x1E" : {
                REG_MAP_NAME : "POWER_STATUS ",
                REG_MAP_SIZE : 1
        },

        "0x1F" : {
                REG_MAP_NAME : "FAULT_STATUS ",
                REG_MAP_SIZE : 1
        },

        "0x20" : {
                REG_MAP_NAME : "EXTENDED_STATUS ",
                REG_MAP_SIZE : 1
        },

        "0x21" : {
                REG_MAP_NAME : "ALERT_EXTENDED ",
                REG_MAP_SIZE : 1
        },

        "0x23" : {
                REG_MAP_NAME : "COMMAND ",
                REG_MAP_SIZE : 1
        },

        "0x24" : {
                REG_MAP_NAME : "DEVICE_CAPABILITIES_1",
                REG_MAP_SIZE : 2
        },

        "0x26" : {
                REG_MAP_NAME : "DEVICE_CAPABILITIES_2",
                REG_MAP_SIZE : 2
        },

        "0x28" : {
                REG_MAP_NAME : "STANDARD_INPUT _CAPABILITIES",
                REG_MAP_SIZE : 1
        },

        "0x29" : {
                REG_MAP_NAME : "STANDARD_OUTPUT _CAPABILITIES",
                REG_MAP_SIZE : 1
        },

        "0x2A" : {
                REG_MAP_NAME : "CONFIG_EXTENDED1 ",
                REG_MAP_SIZE : 1
        },

        "0x2E" : {
                REG_MAP_NAME : "MESSAGE_HEADER _INFO",
                REG_MAP_SIZE : 1
        },

        "0x2F" : {
                REG_MAP_NAME : "RECEIVE_DETECT ",
                REG_MAP_SIZE : 1
        },

        "0x30" : {
                REG_MAP_NAME : "READABLE_BYTE _COUNT",
                REG_MAP_SIZE : 1
        },

        "0x- " : {
                REG_MAP_NAME : "RX_BUF_FRAME_TYPE ",
                REG_MAP_SIZE : 1
        },

        "0x- " : {
                REG_MAP_NAME : "RX_BUF_BYTE_m ",
                REG_MAP_SIZE : 1
        },

        "0x50" : {
                REG_MAP_NAME : "TRANSMIT ",
                REG_MAP_SIZE : 1
        },

        "0x51" : {
                REG_MAP_NAME : "I2C_WRITE_BYTE _COUNT",
                REG_MAP_SIZE : 1
        },

        "0x- " : {
                REG_MAP_NAME : "TX_BUF_BYTE_m ",
                REG_MAP_SIZE : 1
        },

        "0x70" : {
                REG_MAP_NAME : "VBUS_VOLTAGE ",
                REG_MAP_SIZE : 2
        },

        "0x72" : {
                REG_MAP_NAME : "VBUS_SINK_DISCON NECT_THRESHOLD",
                REG_MAP_SIZE : 2
        },

        "0x74" : {
                REG_MAP_NAME : "VBUS_STOP_DIS CHARGE_THRESHOLD",
                REG_MAP_SIZE : 2
        },

        "0x76" : {
                REG_MAP_NAME : "VBUS_VOLTAGE _ALARM_HI_CFG",
                REG_MAP_SIZE : 2
        },

        "0x78" : {
                REG_MAP_NAME : "VBUS_VOLTAGE _ALARM_LO_CFG",
                REG_MAP_SIZE : 2
        },

        "0xC0" : {
                REG_MAP_NAME : "GPIO_DATA_IN_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC1" : {
                REG_MAP_NAME : "GPIO_DATA_OUT_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC2" : {
                REG_MAP_NAME : "GPIO_DIR_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC3" : {
                REG_MAP_NAME : "GPIO_OD_SEL_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC4" : {
                REG_MAP_NAME : "GPIO_ALERT_RISE_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC5" : {
                REG_MAP_NAME : "GPIO_ALERT_FALL_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC6" : {
                REG_MAP_NAME : "GPIO_ALERT_LEVEL_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC7" : {
                REG_MAP_NAME : "GPIO_ALERT_MASK_0 ",
                REG_MAP_SIZE : 1
        },

        "0xC8" : {
                REG_MAP_NAME : "GPIO_DATA_IN_1 ",
                REG_MAP_SIZE : 1
        },

        "0xC9" : {
                REG_MAP_NAME : "GPIO_DATA_OUT_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCA" : {
                REG_MAP_NAME : "GPIO_DIR_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCB" : {
                REG_MAP_NAME : "GPIO_OD_SEL_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCC" : {
                REG_MAP_NAME : "GPIO_ALERT_RISE_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCD" : {
                REG_MAP_NAME : "GPIO_ALERT_FALL_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCE" : {
                REG_MAP_NAME : "GPIO_ALERT_LEVEL_1 ",
                REG_MAP_SIZE : 1
        },

        "0xCF" : {
                REG_MAP_NAME : "GPIO_ALERT_MASK_1 ",
                REG_MAP_SIZE : 1
        },

        "0xD0" : {
                REG_MAP_NAME : "MUX_CONTROL ",
                REG_MAP_SIZE : 1
        },

        "0xD1" : {
                REG_MAP_NAME : "CONTROL_POLARITY ",
                REG_MAP_SIZE : 1
        },

        "0xD2" : {
                REG_MAP_NAME : "CONTROL_OUT_EN ",
                REG_MAP_SIZE : 1
        },

        "0xD3" : {
                REG_MAP_NAME : "CONTROL_OD_SEL ",
                REG_MAP_SIZE : 1
        },

        "0xD4" : {
                REG_MAP_NAME : "GPIO_ALERT_STAT_0 ",
                REG_MAP_SIZE : 1
        },

        "0xD5" : {
                REG_MAP_NAME : "GPIO_ALERT_STAT_1 ",
                REG_MAP_SIZE : 1
        },

        "0xD6" : {
                REG_MAP_NAME : "VC_FAULT_STS ",
                REG_MAP_SIZE : 1
        },

        "0xD7" : {
                REG_MAP_NAME : "VBC_FAULT_CTL ",
                REG_MAP_SIZE : 1
        },

        "0xD8" : {
                REG_MAP_NAME : "LOW_POWER_CFG_1 ",
                REG_MAP_SIZE : 1
        },

        "0xD9" : {
                REG_MAP_NAME : "LOW_POWER_CFG_2 ",
                REG_MAP_SIZE : 1
        },

        "0xDA" : {
                REG_MAP_NAME : "VBUS_OVP_THR_CFG ",
                REG_MAP_SIZE : 2
        },

        "0xDC" : {
                REG_MAP_NAME : "MISC_CTL ",
                REG_MAP_SIZE : 1
        },

        "0xDE" : {
                REG_MAP_NAME : "SW_RST_CTL ",
                REG_MAP_SIZE : 1
        },
}