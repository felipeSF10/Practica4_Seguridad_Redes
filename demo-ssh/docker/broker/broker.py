from flask import Flask, jsonify
import os
from os import remove
from flask import request
import hashlib
from uuid import uuid4
from threading import *
import json
import requests


#Creamos la API con Flask
app = Flask(__name__)
app.secret_key = "myserver.local"
VERSION = "1.0.1"
URL_AUTH = "https://10.0.2.3:5000"
URL_FILES = "https://10.0.2.4:5000" 

def _req(path, URL, data=None, method="GET", verify=False, check=False, token=None):
    if data:
        data = json.dumps(data)

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.request(method, f"{URL}/{path}", data=data, headers=headers, verify=verify)
    print(r.text)
    if check:
        r.raise_for_status()
    return r

class Version():
    @app.route('/version', methods = ['GET'])#ruta de la funcion
    def Version_GET():
        return jsonify({"version": VERSION})

class Login():
    @app.route('/login', methods = ['POST'])#ruta de la funcion
    def Login_POST():
        user = request.get_json().get('username','')
        passw = request.get_json().get('password', '')
        r = _req("login", URL_AUTH, data={"username": user, "password": passw}, method="POST", verify='/certificados/auth.pem')
        if r.status_code != 200:
            return jsonify({"Error": "La contrasena o el usuario es incorrecto"}), 400
        return jsonify(access_token = r.json())

    @app.route('/signup', methods = ['POST'])#ruta de la funcion
    def Signup_POST():
        user = request.get_json().get('username','')
        passw = request.get_json().get('password', '')
        r = _req("signup", URL_AUTH, data={"username": user, "password": passw}, method="POST", verify='/certificados/auth.pem')
        #r = requests.post(URL + "/signup",json={"username":user, "password": passw}, verify='/certificados/auth.pem')
        print("Respuesta de Authenticator: ",r.status_code)
        if r.status_code != 200:
            return jsonify({"Error": "La contrasena o el usuario es incorrecto"}), 400
        return jsonify(access_token = r.json())


if __name__ == '__main__':
    # __init__()
    context = ('/certificados/broker.pem','/certificados/brokerkey2.pem') #ruta del certificado y de la key
    app.run(host = '10.0.1.4',debug = True, ssl_context=context)  