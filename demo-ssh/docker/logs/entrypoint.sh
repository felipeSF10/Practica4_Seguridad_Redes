#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
 
# Permitir acceso SSH para el usuario op
iptables -A INPUT -m owner --uid-owner op -j ACCEPT
iptables -A INPUT -m owner --uid-owner dev -j ACCEPT

#SSH
iptables -A INPUT -p tcp --dport 22 -i eth0 -s 10.0.3.3 -j ACCEPT

ip route del default
ip route add default via 10.0.3.2 dev eth0

service ssh start
service rsyslog start

service rsyslog restart
service fail2ban restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi