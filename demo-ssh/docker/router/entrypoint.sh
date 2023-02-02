#!/bin/bash

echo 1 > /proc/sys/net/ipv4/ip_forward

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

iptables -A INPUT -i lo -j ACCEPT

iptables -A INPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -p icmp -j MASQUERADE

iptables -A FORWARD -i eth0 -o eth1 -p tcp --syn --dport 22 -m state --state NEW -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 22 -j DNAT --to-destination 10.0.1.3
iptables -t nat -A POSTROUTING -o eth1 -p tcp --dport 22 -s 172.17.0.0/16 -d 10.0.1.3 -j SNAT --to-source 10.0.1.2

# #Prueba 443
# iptables -A FORWARD -p tcp --dport 443 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
# iptables -A FORWARD -p tcp --sport 443 -m state --state ESTABLISHED,RELATED -j ACCEPT
# iptables -A FORWARD -i eth0 -o eth1 -p tcp --syn --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
# iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j DNAT --to-destination 10.0.1.4
# iptables -t nat -A POSTROUTING -o eth1 -p tcp --dport 443 -s 172.17.0.0/16 -d 10.0.1.4 -j SNAT --to-source 10.0.1.2

iptables -A FORWARD -i eth0 -o eth1 -p tcp --syn --dport 5000 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 5000 -j DNAT --to-destination 10.0.1.4
iptables -t nat -A POSTROUTING -o eth1 -p tcp --dport 5000 -s 172.17.0.0/16 -d 10.0.1.4 -j SNAT --to-source 10.0.1.2


#Puerto 5000 Servicios API 
# dmz a srv
iptables -A FORWARD -i eth1 -o eth3 -p tcp --dport 5000 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth3 -p tcp --sport 5000 -j ACCEPT
# srv a dmz
iptables -A FORWARD -i eth3 -o eth1 -p tcp --sport 5000 -j ACCEPT 
iptables -A FORWARD -i eth3 -o eth1 -p tcp --dport 5000 -j ACCEPT 

#Puerto 22 SSH
# Work
iptables -A INPUT -p tcp --dport 22 -i eth2 -s 10.0.3.3 -j ACCEPT
# dev a srv
iptables -A FORWARD -i eth2 -o eth3 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth3 -p tcp --sport 22 -j ACCEPT
# srv a dev
iptables -A FORWARD -i eth3 -o eth2 -p tcp --sport 22 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth2 -p tcp --dport 22 -j ACCEPT
# dmz a dev
iptables -A FORWARD -i eth1 -o eth2 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth2 -p tcp --sport 22 -j ACCEPT
# dev a dmz
iptables -A FORWARD -i eth2 -o eth1 -p tcp --dport 22 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -p tcp --sport 22 -j ACCEPT


#Puerto 514 Rsyslog
#Red dmz
iptables -A INPUT -p udp -i eth1 --dport 514 -s 10.0.1.0/24 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth3 -p udp --dport 514 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth1 -p udp --sport 514 -j ACCEPT

#Red srv
iptables -A INPUT -p udp -i eth3 --dport 514 -s 10.0.2.0/24 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth3 -p udp --dport 514 -j ACCEPT

#Red dev
iptables -A INPUT -p udp -i eth2 --dport 514 -s 10.0.3.0/24 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth3 -p udp --dport 514 -j ACCEPT
iptables -A FORWARD -i eth3 -o eth2 -p udp --sport 514 -j ACCEPT

service ssh start
service rsyslog start

service fail2ban restart

if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi
