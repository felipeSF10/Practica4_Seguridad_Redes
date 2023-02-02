#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT
 
# Permitir acceso SSH para el usuario op
# iptables -A INPUT -m owner --uid-owner op -j ACCEPT
# iptables -A INPUT -m owner --uid-owner dev -j ACCEPT

iptables -A INPUT -p tcp --dport 22 -s 10.0.1.3 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.2.0/24 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -s 10.0.3.0/24 -j ACCEPT

ip route del default
ip route add default via 10.0.3.2 dev eth0

service ssh start
service rsyslog start

# echo "PermitRootLogin no" >> /etc/ssh/sshd_config
# echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
echo "dev ALL=(ALL) ALL" | sudo tee -a /etc/sudoers

service rsyslog restart
service fail2ban restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
