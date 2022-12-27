#!/bin/bash

ip route add 10.0.1.0/24 via 10.0.2.2

echo "10.0.2.3    auth" >> /etc/hosts
echo "10.0.2.4    files" >> /etc/hosts


if [ -z "$@" ]; then
    exec /bin/bash
else
    exec $@
fi