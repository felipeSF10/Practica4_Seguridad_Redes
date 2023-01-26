FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip

#COPY authorized_keys /home/jump/.ssh/authorized_keys
RUN pip3 install flask flask_restful requests


COPY entrypoint.sh /entrypoint.sh

COPY certificados ./certificados
COPY ./certificados/files.pem ./usr/local/share/ca-certificates/cert.crt
RUN sudo update-ca-certificates

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]