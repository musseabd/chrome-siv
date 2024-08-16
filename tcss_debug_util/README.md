Full doc at:
https://intel.sharepoint.com/:w:/r/sites/ccgcpeclss/Shared%20Documents/Chrome%20SIV/Common/Tools/TCSS_Debug_Utility.docx?d=wb0834782f4e3467eab90ca884a125d3f&csf=1&web=1&e=i20a7n

# 1. How to get/download the tool

```
git clone https://github.com/musseabd/chrome-siv.git

cd tcss_debug_util
```

# 2. How to use the tool

Tool has 2 main components. There are other scripts for convenience as well.

## 2.1 Main components

### 2.1.1 collect_logs_dut.sh

* Description
  * runs on DUT
  * Dumps output of all the commands from debug manual into a log file. This log file will be input to analyze_log.py
* Input: none
* Output: dut_log.txt
* Usage
  * collect_logs_dut.sh --help

### 2.1.2 analyze_log.py

* Description
  * runs on DUT or Host
  * For each TCSS sub-domain, points out potential sources of issues
* Input: dut_log.txt, type_c_device, port_num
* Output: result of auto analysis
* Usage
  * analyze_log.py --help

## 2.2 Scripts for convinience

### 2.2.1 get_log_from_dut.sh

* Description
  * runs on Host
  * Dumps log on dut and copy the log back to host
* Input: dut_ip, type_c_device, port_num
* Usage
  * get_log_from_dut.sh --help

### 2.2.2 debug_live.sh

* Description
  * runs on Host
  * Copies and runs collect_logs_dut.sh on dut, copies log back to host and runs analyze_log.py on it
* Input: dut_ip, type_c_device, port_num
* Usage
  * debug_live.sh --help
