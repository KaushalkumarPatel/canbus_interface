setCanBitRate() {
	if [ $# -ne 2 ]; then
		echo "usage: canbaud <can interface> <baud>"
		return
	fi
	echo $1 $2
	sudo ifconfig $1 down
	echo $?
	sudo ip link set $1 type can bitrate $2
	echo $?
	sudo ifconfig $1 up
	echo $?
}
alias canbaud='setCanBitRate'

checkCanBitRate() {
	if [ $# -ne 1 ]; then 
		echo "usage: iscanup <can interface>"
		return
	fi 
	if [ `candump -T 1000 -n 4 $1 |wc -l`  -ne 0 ]; then
		echo "traffic";
	else
		echo "no traffic";
	fi
}
alias iscanup='checkCanBitRate'
alias showcanbaud='ip -details link show' 
