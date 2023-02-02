FROM debian

RUN apt-get update && \
    apt-get install -y \
	iptables \
	iproute2 \
	net-tools \
	tcpdump \
	iputils-ping \
	nano \
 	less \
	openssh-server \
	fail2ban \
	rsyslog \
	curl \
	sudo \
	&& \
    apt-get clean

COPY assets/sshd_config /etc/ssh/sshd_config
RUN chmod 644 /etc/ssh/sshd_config && \
    useradd -ms /bin/bash op && \
    mkdir /home/op/.ssh && \
    chmod 700 /home/op/.ssh

COPY assets/authorized_keys.op /home/op/.ssh/authorized_keys
RUN chmod 644 /home/op/.ssh/authorized_keys

COPY assets/sudoers.op /etc/sudoers.d
RUN chown op:op -R /home/op

COPY assets/sudoers.op /etc/sudoers.d/op
COPY fail2ban/jail.conf /etc/fail2ban/jail.local