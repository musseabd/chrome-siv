
validatie_device () {
	device=$1

	valid_device_list="DP_DOCK|DP_CABLE|USB|TBT3|TBT4_USB4"

	case $device in
		DP_DOCK|DP_CABLE|USB|TBT3|TBT4_USB4)
		;;

		*)
		echo "device has to be one of $valid_device_list"
	esac
}