FROM midebian

RUN apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install flask flask_restful requests

COPY entrypoint.sh /entrypoint.sh
COPY files.py files.py

RUN mkdir usuarios

COPY certificados ./certificados

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]