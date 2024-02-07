

'''
0x10
ALERT
2 Bytes

0x1 << 0
    CC Status Changed

0x1 << 1
    Power Status Changed

...


'''

registers = {           
    "0x10" : [ # ALERT
        {
            "name" : "Extended Status Changed",
            "mask" : 0x1,
            "shift" : 13,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
        {
            "name" : "VBUS Sink Disconnect Detected",
            "mask" : 0x1,
            "shift" : 11,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
        {
            "name" : "Rx Buffer Overflow",
            "mask" : 0x1,
            "shift" : 10,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
                {
            "name" : "recvd HARD RESET",
            "mask" : 0x1,
            "shift" : 3,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
        {
            "name" : "RECV SOP Buffer Changed",
            "mask" : 0x1,
            "shift" : 2,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
        {
            "name" : "Power Status Changed",
            "mask" : 0x1,
            "shift" : 1,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },
        {
            "name" : "CC Status Changed",
            "mask" : 0x1,
            "shift" : 0,
            "write_1_to_clear" : True,
            "values_str" : ["clear", "set"],
            "last_val_str" : "clear"
        },


    ],

    "0x19" : [ # TCPC CONTROL
        {
            "name" : "Plug Orientation",
            "mask" : 0x1,
            "shift" : 0,
            "values_str" : ["CC2 PD, CC1 Vconn, ", "CC1 PD, CC2 Vconn"],
        },
        {
            "name" : "TCPM in charge of DebugMode",
            "mask" : 0x1,
            "shift" : 4,
            "values_str" : ["ctrl by TCPC", "ctrl by TCPM"]
        },
        {
            "name" : "Enable ALERT.CcStatus assertion when CC_STATUS.Looking4Connection changes",
            "mask" : 0x1,
            "shift" : 6,
            "values_str" : ["clear", "set"]
        }        
    ],

    "0x1A" : [ # ROLE CONTROL
        {
            "name" : "RP Value",
            "mask" : 0x3,
            "shift" : 4,
            "values_str" : ["Rp default", "Rp 1.5A", "Rp 3.0A", "Reserved",]
        },
        {
            "name" : "CC2",
            "mask" : 0x3,
            "shift" : 2,
            "values_str" : ["Ra", "Rp", "Rd", "Open"]
        },
        {
            "name" : "CC1",
            "mask" : 0x3,
            "shift" : 0,
            "values_str" : ["Ra", "Rp", "Rd", "Open"]
        }
    ],

    "0x1D" : [ # CC STATUS
        {
            "name" : "Looking4Connection",
            "mask" : 0x1,
            "shift" : 5,
            "values_str" : ["TCPC is not actively looking for a connection", "TCPC is looking for a connection"]
        },
        {
            "name" : "ConnectResult",
            "mask" : 0x1,
            "shift" : 4,
            "values_str" : ["TCPC is presenting Rp", "TCPC is presenting Rd"]
        },
        {
            "name" : "CC2 State",
            "mask" : 0x3,
            "shift" : 2,
            "values_str" : ["SRC/SNK...", "SRC/SNK...", "SRC/SNK...", "SRC/SNK..."]
        },
        {
            "name" : "CC1 State",
            "mask" : 0x3,
            "shift" : 0,
            "values_str" : ["SRC/SNK...", "SRC/SNK...", "SRC/SNK...", "SRC/SNK..."]
        }
    ],

    "0x2F" : [ # RECEIVE_DETECT
        {
            "name" : "Enable Hard Reset",
            "mask" : 0x1,
            "shift" : 5,
            "values_str" : ["clear", "set"]
        },
        {
            "name" : "Enable SOPDBG'",
            "mask" : 0x1,
            "shift" : 3,
            "values_str" : ["clear", "set"]
        },
        {
            "name" : "Enable SOP\"",
            "mask" : 0x1,
            "shift" : 2,
            "values_str" : ["clear", "set"]
        },
        {
            "name" : "Enable SOP'",
            "mask" : 0x1,
            "shift" : 1,
            "values_str" : ["clear", "set"]
        },
        {
            "name" : "Enable SOP",
            "mask" : 0x1,
            "shift" : 0,
            "values_str" : ["clear", "set"]
        },
    ]        
}

def reg_fields_print(addr_str, byte_array, reg_rw_str):
    '''
    eg. reg_fields_print("0x10", [0x1, 0x0]) # b/c ALERT is a two byte register
    '''
        
    fields = registers.get(addr_str)

    if addr_str == "0x10":
        x = 2

    if fields == None or len(fields) == 0:
        return False

    reg_int = 0
    # for int_ in byte_array:
    #     reg_int = reg_int | int_
    for i in range(len(byte_array)):
        reg_int |= byte_array[i] << (i*8)
    
    printed_fields = reg_int
    for field in fields:
        mask = field["mask"]
        shift = field["shift"]

        printed_fields &= ~(mask << shift)

        field_val = (reg_int & (mask<<shift)) >> shift        
        field_val_str = field["values_str"][field_val]

        # if write on clear field
        if reg_rw_str == "Write" and field_val == 1 and "write_1_to_clear" in field:
            field_val_str = "clear"

        # for registers like ALERT, only want to print when values are set
        if addr_str == "0x10":
            if field_val:
                print(f"\t{field['name']} : {field_val_str}")
        else:
            print(f"\t{field['name']} : {field_val_str}")

    # one or more set fields not in fields list, so print the raw register bytes
    if printed_fields != 0:
        return False
    
    return True
