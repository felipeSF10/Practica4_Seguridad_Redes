FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip


RUN pip3 install flask flask_restful requests
COPY authenticator.py ./auth/authenticator.py

COPY ./certificados/ ./certificados/



COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]