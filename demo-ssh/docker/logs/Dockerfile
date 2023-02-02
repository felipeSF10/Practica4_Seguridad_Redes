FROM debian

COPY entrypoint.sh /entrypoint.sh
COPY rsyslog.conf /etc/rsyslog/jail.local

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]