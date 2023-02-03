FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install flask flask_restful requests

COPY broker.py broker.py
COPY certificados /certificados

RUN chmod -R 644 certificados
RUN chmod -R 744 broker.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]