#!/bin/bash

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p icmp -j ACCEPT

ip route replace default via 10.0.2.2 dev eth0

iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.2.2 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.2.4 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -i eth0 -s 10.0.1.4 -j ACCEPT

echo "10.0.2.3    auth" >> /etc/hosts
echo "10.0.2.4    files" >> /etc/hosts


service ssh start
service rsyslog start

echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config

service ssh restart
service rsyslog restart

python3 authenticator.py

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi