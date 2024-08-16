import logging

import dut_log


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def val_to_str_default(key, val):
	return str(val)

def print_title(title):
	print(dut_log.log_file_cmd_start_indicator)
	print(f"{title}")
	print(dut_log.log_file_cmd_start_indicator)

def print_result(title:str, test_pass:bool):
	print(dut_log.log_file_cmd_start_indicator)
	pass_or_fail_str = f"{bcolors.OKGREEN}PASS" if test_pass else f"{bcolors.FAIL}FAIL"
	print(f'{pass_or_fail_str} : {title} {bcolors.ENDC}')
	print(dut_log.log_file_cmd_start_indicator)

def print_actual_vs_expected(title, expected, actual, val_to_str=None, attr_width=13):

	if val_to_str == None: val_to_str = val_to_str_default

	print_title(title)

	print("{:<{width}} {:^12} {:^12}".format("", "[expected]", "[actual]", width=attr_width))

	test_pass = True
	
	for key, expected_val in expected.items():
		if key not in actual:
			logging.error("mux_info unknown key: %s", key)
			test_pass = False
			continue

		actual_val = actual[key]

		actual_val_str = val_to_str(key, actual_val)
		expected_val_str = val_to_str(key, expected_val)

		
		#print(f"{key:<13.13} {expected_val_str:^12} {actual_val_str:^12}", end="") # don't print new line in case we print <<< FAIL next to it
		print("{:<{width}.{width}} {:^12} {:^12}".format(key, expected_val_str, actual_val_str, width=attr_width), end="")

		if expected_val != actual[key]:
			test_pass = False
			print(f"{bcolors.FAIL} <<<<<<<<<<<<<<<<<<<<<<<<<<   FAIL {bcolors.ENDC}", end="") # don't print new line to avoid 2 new lines incase of fail
			# raise Exception(f"ec mux_info: expected: {key}:{expected_val} but got {key}:{dut_muxinfo[key]}")

		print()

	print_result(title, test_pass)


def print_result_string_in_cmd_output(title, expected_str, cmd_output):

	print_title(title)

	test_pass = expected_str in cmd_output

	result_str = "expected string {} in cmd output".format("is" if test_pass else "is NOT")
	
	result_str += "" if test_pass else f"{bcolors.FAIL} <<<<<<<<<<<<<<<<<<<<<<<<<<   FAIL {bcolors.ENDC}"

	print(result_str)

	print("expected string:")
	print(expected_str)

	print()
	print("cmd output:")
	print(cmd_output)

	print_result(title, test_pass)

def print_result_all_strings_in_cmd_output(title, strs, cmd_output):

	print_title(title)

	test_pass = True

	for str in strs:
		if str in cmd_output:
			print(f"{str} is in cmd output")
		else:
			print(f"{str} is NOT in cmd output <<<<<<<<<<<<<<<<<<<<<<<<<<   FAIL")
			test_pass = False

	print()
	print("cmd output:")
	print(cmd_output)

	print_result(title, test_pass)
	

