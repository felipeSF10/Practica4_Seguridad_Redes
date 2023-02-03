FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install flask flask_restful requests

COPY authenticator.py authenticator.py
COPY certificados /certificados

RUN chmod -R 644 certificados
RUN chmod -R 744 authenticator.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]