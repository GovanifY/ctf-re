#!/usr/bin/env bash
TUN_INTERFACE="tap${1:-0}"
IP_ADDRESS="10.0.2.1"

# create tuntap interface
ip tuntap add $TUN_INTERFACE mode tap
ip link set dev $TUN_INTERFACE up
ifconfig $TUN_INTERFACE $IP_ADDRESS

# perform trivial redirections
sysctl net.ipv4.ip_forward=1
# give Internet to the VMs.
iptables -t nat -A POSTROUTING -s 10.0.2.0/24 -j MASQUERADE
