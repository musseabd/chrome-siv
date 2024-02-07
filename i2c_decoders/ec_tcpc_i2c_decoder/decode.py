
import argparse

# parse arguments
parser = argparse.ArgumentParser(description="decode i2c messages between EC and TCPC")
parser.add_argument("input_csv_file")

args = parser.parse_args()

input_file = args.input_csv_file

'''
Read Two Byte Register
    Start
        Address/Write (TCPC 0x73)
            ACK
        Data    (Register Address)
            ACK
    Start
        Address/Read (TCPC 0x73)
        Data    (Reg Value LSB)
            ACK
        Data    (Reg Value MSB)
            NAK
    Stop


Write Two Byte Register
    Start
        Address/Write (TCPC 0x73)
            ACK
        Data    (Register Address)
            ACK
        Data    (Reg Value LSB)
            ACK 
        Data    (Reg Value MSB)
            ACK
    Stop

Read RECV Buffer
    Start
        Address/Write (TCPC 0x73)
            ACK
        Data    (Register Address 0x30)
            ACK
    Start
        Address/Read (TCPC 0x73)
        Data    (Readable Bytes Count Including this)
            ACK
        Data X (READABLE_COUNT - 2) (RECV Byte)
            ACK
        Data
            NAK
    Stop
    
Write TX Buffer
    Start
        Address/Write (TCPC 0x73)
            ACK
        Data    (Register Address 0x50)
            ACK
        Data    (Writable Bytes Count Including this)
            ACK
        Data X (WRITABLE_COUNT - 2) (Tx Byte)
            ACK
        Data
            NAK
    Stop
'''
from reg_map import *
from reg_fields import *

## section: macros and constants

STATE_SEND_START = "STATE_WAIT_FOR_START"
STATE_SEND_TCPC_ADDR_AND_WRITE = "STATE_SEND_TCPC_ADDR_AND_WRITE"
STATE_SEND_REG_ADDR = "STATE_SEND_REG_ADDR" # here we can know if 1 Byte, 2 Byte, recv_buff, tx_buff

STATE_WRITE_DATA_OR_SEND_REPEATED_START = "STATE_WRITE_DATA_OR_SEND_REPEATED_START"

# writing a register
STATE_WRITE_REG_BYTES = "STATE_WRITE_REG_BYTES"
# reading a register
STATE_SEND_REPEATED_START = "STATE_SEND_REPEATED_START"
STATE_SEND_TCPC_ADDR_AND_READ = "STATE_SEND_TCPC_ADDR_AND_READ"
STATE_READ_REG_BYTES = "STATE_READ_REG_BYTES" # last read byte should be NAK'ed

STATE_SEND_STOP = "STATE_SEND_STOP"


CSV_HEADER_TYPE = "type"
CSV_HEADER_START_TIME = "start_time"
CSV_HEADER_ACK  = "ack"
CSV_HEADER_ADDRESS  = "address"
CSV_HEADER_RW   = "read"
CSV_HEADER_DATA   = "data"
CSV_HEADER_ERROR = "error"

CSV_TYPE_START = "start"
CSV_TYPE_STOP = "stop"
CSV_TYPE_ADDRESS = "address"
CSV_TYPE_DATA = "data"

CSV_ACK_ACK = "true"
CSV_ACK_NAK = "false"

CSV_RW_READ = "true"
CSV_RW_WRITE = "false"
CSV_RW_NONE = ""

CSV_ERROR_NONE = ""

TCPC_I2C_ADDR = "0x73"
NONE_I2C_ADDR = ""

_err_str = ""

## section: global variables (global to this file)
_curr_reg = {}

_tcpc_reg = []

_tcpc_reg_access_start_time = ""
_tcpc_reg_access_stop_time = ""
_tcpc_reg_rw = ""

def tcpc_reg_print():
    for byte in _tcpc_reg:
        print(f"\t{hex(byte)}")

def tcpc_reg_add_byte(byte):    
    _tcpc_reg.append(int(byte, 16))

def state_send_start(line):
    global _err_str
    global _tcpc_reg_access_start_time

    error = False
    next_state = STATE_SEND_START

    if line[CSV_HEADER_TYPE] == CSV_TYPE_START:
        next_state = STATE_SEND_TCPC_ADDR_AND_WRITE

        _tcpc_reg_access_start_time = line[CSV_HEADER_START_TIME]
    else:
        error = True
        _err_str = "skipped line waiting for start"

    return error, next_state


def state_send_tcpc_addr_and_write(line):
    global _err_str

    error = False
    next_state = STATE_SEND_TCPC_ADDR_AND_WRITE

    if line[CSV_HEADER_TYPE] == CSV_TYPE_ADDRESS and\
        line[CSV_HEADER_ACK] == CSV_ACK_ACK and\
        line[CSV_HEADER_ADDRESS] == TCPC_I2C_ADDR and\
        line[CSV_HEADER_RW] == CSV_RW_WRITE and\
        line[CSV_HEADER_ERROR] == CSV_ERROR_NONE:
        next_state = STATE_SEND_REG_ADDR
    else:
        error = True
        next_state = STATE_SEND_START

        _err_str = f"expected: {CSV_TYPE_ADDRESS}, {CSV_ACK_ACK}, {TCPC_I2C_ADDR}, {CSV_RW_WRITE}, {CSV_ERROR_NONE}\n\
            got: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"

    return error, next_state


def state_send_reg_addr(line):
    global _err_str
    global _curr_reg

    error = False
    next_state = STATE_SEND_REG_ADDR

    if line[CSV_HEADER_TYPE] == CSV_TYPE_DATA and\
        line[CSV_HEADER_ACK] == CSV_ACK_ACK and\
        line[CSV_HEADER_ADDRESS] == "" and\
        line[CSV_HEADER_RW] == CSV_RW_NONE and\
        line[CSV_HEADER_ERROR] == CSV_ERROR_NONE:

        next_state = STATE_WRITE_DATA_OR_SEND_REPEATED_START

        reg_addr = line[CSV_HEADER_DATA]
        _curr_reg = reg_map.get(reg_addr)

        if _curr_reg == None:
            error = True
            next_state = STATE_SEND_START

            _err_str = f"register {reg_addr} not in reg_map"
        else:
            _curr_reg[REG_MAP_ADDR] = reg_addr # TODO: find a better way of doing this

    else:
        error = True
        next_state = STATE_SEND_START

        _err_str = f"expected: {CSV_TYPE_DATA}, {CSV_ACK_ACK}, {NONE_I2C_ADDR}, {CSV_RW_NONE}, {CSV_ERROR_NONE}\n\
            got: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"
  

    return error, next_state


def state_write_data_or_send_repeated_start(line):
    global _err_str
    global _tcpc_reg_rw

    error = False
    next_state = STATE_WRITE_DATA_OR_SEND_REPEATED_START

    # if its data, EC is writing to register/buffer
    if line[CSV_HEADER_TYPE] == CSV_TYPE_DATA and\
        line[CSV_HEADER_ACK] == CSV_ACK_ACK and\
        line[CSV_HEADER_ADDRESS] == "" and\
        line[CSV_HEADER_RW] == CSV_RW_NONE and\
        line[CSV_HEADER_ERROR] == CSV_ERROR_NONE:

        _tcpc_reg_rw = "Write"

        data = line[CSV_HEADER_DATA]
        tcpc_reg_add_byte(data)

        # for writing TCPC tx buffer, the first date(byte) tells us the size of buff
        if  _curr_reg[REG_MAP_ADDR] == "0x50" and len(_tcpc_reg) == 1:
            _curr_reg[REG_MAP_SIZE] = int(data, 16) + 1 # +1 to include the BYTE_COUNT itself

        # if 1 byte register we are done writing
        if _curr_reg[REG_MAP_SIZE] == 1:            
            next_state = STATE_SEND_STOP
        # else continue writing the rest of bytes
        else:
            next_state = STATE_WRITE_REG_BYTES
    
    # else if its a repeated start, EC is reading register/buffer
    elif line[CSV_HEADER_TYPE] == CSV_TYPE_START:              
        next_state = STATE_SEND_TCPC_ADDR_AND_READ
    else:
        error = True
        next_state = STATE_SEND_START

        _err_str = f"expected: {CSV_TYPE_DATA}|{CSV_TYPE_START}, {CSV_ACK_ACK}, "", {CSV_RW_NONE}, {CSV_ERROR_NONE}\n\
            got: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"
  

    return error, next_state

def state_send_tcpc_addr_and_read(line):
    global _err_str
    global _tcpc_reg_rw

    error = False
    next_state = STATE_SEND_TCPC_ADDR_AND_READ

    if line[CSV_HEADER_TYPE] == CSV_TYPE_ADDRESS and\
        line[CSV_HEADER_ACK] == CSV_ACK_ACK and\
        line[CSV_HEADER_ADDRESS] == TCPC_I2C_ADDR and\
        line[CSV_HEADER_RW] == CSV_RW_READ and\
        line[CSV_HEADER_ERROR] == CSV_ERROR_NONE:

        _tcpc_reg_rw = "Read"

        next_state = STATE_READ_REG_BYTES
    else:
        error = True
        next_state = STATE_SEND_START

        _err_str = f"expected: {CSV_TYPE_DATA}, {CSV_ACK_ACK}, {TCPC_I2C_ADDR}, {CSV_RW_READ}, {CSV_ERROR_NONE}\n\
            got: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"
  

    return error, next_state

def state_write_reg_bytes(line):
    global _err_str

    error = False
    next_state = STATE_WRITE_REG_BYTES

    # if its data, EC is writing to register/buffer
    if line[CSV_HEADER_TYPE] == CSV_TYPE_DATA and\
        line[CSV_HEADER_ACK] == CSV_ACK_ACK and\
        line[CSV_HEADER_ADDRESS] == NONE_I2C_ADDR and\
        line[CSV_HEADER_RW] == CSV_RW_NONE and\
        line[CSV_HEADER_ERROR] == CSV_ERROR_NONE:

        data = line[CSV_HEADER_DATA]
        tcpc_reg_add_byte(data)

        # if we have read all TCPC reg bytes
        if _curr_reg[REG_MAP_SIZE] == len(_tcpc_reg):            
            next_state = STATE_SEND_STOP
    
    # else if its a repeated start, EC is reading register/buffer
    elif line[CSV_HEADER_TYPE] == CSV_TYPE_START:              
        next_state = STATE_SEND_TCPC_ADDR_AND_READ
    else:
        error = True
        next_state = STATE_SEND_START

        _err_str = f"expected: {CSV_TYPE_DATA}, {CSV_ACK_ACK}, {NONE_I2C_ADDR}, {CSV_RW_NONE}, {CSV_ERROR_NONE}\n\
            got: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"
  

    return error, next_state

def state_read_reg_bytes(line):
    global _err_str

    error = False
    next_state = STATE_READ_REG_BYTES

    expected_type = CSV_TYPE_DATA
    expected_ack = "not yet known"
    expected_i2c_addr = ""
    expected_rw     = CSV_RW_NONE
    expected_error = ""

    # if its data, EC is writing to register/buffer
    if line[CSV_HEADER_TYPE] == expected_type and\
        line[CSV_HEADER_RW] == expected_rw and\
        line[CSV_HEADER_ERROR] == expected_error:

        data = line[CSV_HEADER_DATA]
        tcpc_reg_add_byte(data)        

        # for TCPC recv buffer, first byte tells us the readable byte count
        if  _curr_reg[REG_MAP_ADDR] == "0x30" and len(_tcpc_reg) == 1:
            _curr_reg[REG_MAP_SIZE] = int(data, 16) + 1 # +1 to include the BYTE_COUNT itself

        expected_ack = CSV_ACK_ACK if _curr_reg[REG_MAP_SIZE] > len(_tcpc_reg) else CSV_ACK_NAK

        # last read must be NAK'ed by EC
        if line[CSV_HEADER_ACK] != expected_ack:
            error = True
            next_state = STATE_SEND_START
        else:
            # if we have read all TCPC reg bytes
            if _curr_reg[REG_MAP_SIZE] == len(_tcpc_reg):            
                next_state = STATE_SEND_STOP
    
    # else if its a repeated start, EC is reading register/buffer
    elif line[CSV_HEADER_TYPE] == CSV_TYPE_START:              
        next_state = STATE_SEND_TCPC_ADDR_AND_READ
    else:
        error = True
        next_state = STATE_SEND_START

    
    if error:
        _err_str = (f"\texpected: {CSV_TYPE_DATA}, {expected_ack}, {expected_i2c_addr}, {expected_rw}, {expected_error}\n"
            f"\tgot: {line[CSV_HEADER_TYPE]}, {line[CSV_HEADER_ACK]}, {line[CSV_HEADER_ADDRESS]}, {line[CSV_HEADER_RW]}, {line[CSV_HEADER_ERROR]}"
            )


    return error, next_state

def state_send_stop(line):
    global _tcpc_reg_access_stop_time

    error = False
    next_state = STATE_SEND_STOP

    if line[CSV_HEADER_TYPE] == CSV_TYPE_STOP:
        next_state = STATE_SEND_START

        _tcpc_reg_access_stop_time = line[CSV_HEADER_START_TIME] # not a bug

        print(f"{_tcpc_reg_rw} {_curr_reg[REG_MAP_NAME]} [{_curr_reg[REG_MAP_ADDR]}] line: {_csv_line_no} time: {line[CSV_HEADER_START_TIME]}")
        # print(f"\tline: {_csv_line_no} start: {_tcpc_reg_access_start_time} stop: {_tcpc_reg_access_stop_time}")
        print(f"\tduration: {(float(_tcpc_reg_access_stop_time) - float(_tcpc_reg_access_start_time))* (10**6)} us")
        
        # print field names if available, if not print raw register values
        if not reg_fields_print(_curr_reg[REG_MAP_ADDR], _tcpc_reg, _tcpc_reg_rw):
            tcpc_reg_print()

    return error, next_state



_csv_line_no = 2
def error_critical(str):    
    print(f"line num: {_csv_line_no}")
    print(str)
    exit()

_state = STATE_SEND_START

def run_tcpci_state(line):
    global _state
    error = False
    next_state = _state

    if _state == STATE_SEND_START:
        error, next_state = state_send_start(line)
    elif _state == STATE_SEND_TCPC_ADDR_AND_WRITE:
        error, next_state = state_send_tcpc_addr_and_write(line)
    elif _state == STATE_SEND_REG_ADDR:
        error, next_state = state_send_reg_addr(line)
    elif _state == STATE_WRITE_DATA_OR_SEND_REPEATED_START:
        error, next_state = state_write_data_or_send_repeated_start(line)
    elif _state == STATE_SEND_TCPC_ADDR_AND_READ:
        error, next_state = state_send_tcpc_addr_and_read(line)
    elif _state == STATE_WRITE_REG_BYTES:
        error, next_state = state_write_reg_bytes(line)
    elif _state == STATE_READ_REG_BYTES:
        error, next_state = state_read_reg_bytes(line)
    elif _state == STATE_SEND_STOP:
        error, next_state = state_send_stop(line)
    else:
        error_critical(f"state {_state} not implemented")

    # state change
    if _state != next_state:
        if error:
            print(f"error processing line {_csv_line_no}")
            print(_err_str)
        # print(f"line {_csv_line_no} {_state} ==> {next_state}")

        if next_state == STATE_SEND_START:
            _tcpc_reg.clear()

        _state = next_state

    return error


## section csv
import csv
_i2c_capture = []
_i2c_capture_iter = []

with open(input_file, mode ='r')as file:
    csv_dict_reader = csv.DictReader(file)

    for row in csv_dict_reader:
        _i2c_capture.append(row)

    _i2c_capture_iter = iter(_i2c_capture)

def get_next_line():
    global _i2c_capture_iter

    line = next(_i2c_capture_iter, None)
    return line


# TODO: report time taken to read/write registesr and flag ones that break TCPCI timing requirement

_start_time_sec = "77.570"
_end_time_sec = "79.287"
line = get_next_line()
while line:    
    # print(f"line: {_csv_line_no}")
    # print(line)

    if float(line[CSV_HEADER_START_TIME]) >= float(_start_time_sec) and\
        float(line[CSV_HEADER_START_TIME]) <= float(_end_time_sec):
       
        error = run_tcpci_state(line)

        # if unexpected line happens state machine goes to its initial state
        # run state machine once more to see if this line is a fresh start
        # if its not a fresh start, then we will just print the bad line
        # and move on
        if error:
            error = run_tcpci_state(line)
            if error:
                print(f"bad line # {_csv_line_no}")

    line = get_next_line()
    _csv_line_no += 1 # helps to find where in the csv file we are



