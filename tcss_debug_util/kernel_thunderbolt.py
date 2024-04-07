




#def ec_check_mux(port, connected_device):
	# 1. check typecd log to see if port entered TBT mode
	# get the last line in /var/log/typecd.log that has "mode on port <port#>"
	#_check_typecd_log(port)

	# 2. check if thunderbolt enumerated under /sys/bus/thunderbolt
	# example: ls /sys/bus/thunderbolt/devices
	# 	0-0
	# 	1-0
	