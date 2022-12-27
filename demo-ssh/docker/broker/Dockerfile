FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip

#COPY authorized_keys /home/jump/.ssh/authorized_keys
RUN pip3 install flask flask_restful requests
COPY broker.py ./broker/broker.py
COPY ./certificados/ ./certificados/


COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]