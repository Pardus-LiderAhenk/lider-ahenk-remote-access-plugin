#!/bin/bash
if [ $# -lt 1 ]; then
	echo "Usage: remote_desktop.sh <passwd> <port> <display_no[0]> ";
	echo "Example: remote_desktop.sh 111 5999 0"
	exit 1;
fi
port="5999";
if [ $# -gt 1 ]; then
	port=$2
fi
display="0";
if [ $# -gt 2 ]; then
	display=$3
fi
if ! which x11vnc > /dev/null; then
	apt-get install -y x11vnc
fi
w -oush | awk '{print $1, $3}' | while read x; do 
	array=(${x//:/ })
	if [ $display -eq ${array[1]} ]; then
		echo "username: ${array[0]} at display $display"
		ps aux | grep x11vnc | grep "port $port" | awk '{print $2}' | xargs kill -9
		su - ${array[0]} -c "mkdir -p /tmp/.vncahenk${array[0]}"
		su - ${array[0]} -c "x11vnc -storepasswd $1 /tmp/.vncahenk${array[0]}/x11vncpasswd"
		su - ${array[0]} -c "x11vnc -accept 'popup' -rfbport $port -rfbauth /tmp/.vncahenk${array[0]}/x11vncpasswd -o /tmp/.vncahenk${array[0]}/vnc.log -display :$display &"
		exit 0
	fi
done

