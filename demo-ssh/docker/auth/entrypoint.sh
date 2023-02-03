#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

#Remplazar la ruta predeterminada al gateway
ip route replace default via 10.0.2.2 dev eth0

#Puerto 5000 Servicios API 
iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.2.2 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.2.4 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.1.4 -j ACCEPT

#SSH
iptables -A INPUT -p tcp --dport 22 -i eth0 -s 10.0.3.3 -j ACCEPT

service ssh start
service rsyslog start

service fail2ban restart

python3 authenticator.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi