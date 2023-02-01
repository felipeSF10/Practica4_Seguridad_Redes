FROM debian

COPY entrypoint.sh /entrypoint.sh
COPY rsyslog.conf /etc/resyslog.d/jail.local

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]