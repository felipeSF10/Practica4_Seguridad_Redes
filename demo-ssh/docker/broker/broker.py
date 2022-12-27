from flask import Flask, jsonify
import os
from os import remove
from flask import request
import hashlib
from uuid import uuid4
from threading import *
import json


#Creamos la API con Flask
app = Flask(__name__)
app.secret_key = "myserver.local"
VERSION = "1.0.1"

class Version():
    @app.route('/version', methods = ['GET'])#ruta de la funcion
    def Version_GET():
        return jsonify({"version": VERSION})

if __name__ == '__main__':
    # __init__()
    context = ('/certificados/cert.pem','/certificados/key.pem') #ruta del certificado y de la key
    app.run(debug = True, ssl_context=context)  