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
app.secret_key = "10.0.2.4"
URL_AUTH = "https://10.0.2.3:5000"

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

def autenticacion(usuario, token):
    return _req("autenticar", URL_AUTH, data={"username": usuario}, method="POST", verify='/certificados/auth.pem', token=token)
    
class ExploradorDocumentos():
    @app.route('/<string:username>/<string:doc_id>', methods = ['GET', 'POST', 'PUT', 'DELETE'])#ruta de la funcion
    def ExploradorDoc(username, doc_id):
        if request.method == 'GET':
            if doc_id == "_all_docs":
                return all_docs_GET(username)
            else:
                return Doc_GET(username, doc_id)
        elif request.method == 'POST':
            return Doc_POST(username, doc_id)  
        elif request.method == 'PUT':
            return Doc_PUT(username, doc_id)
        elif request.method == 'DELETE':
            return Doc_DELETE(username, doc_id)

def all_docs_GET(username):
    auth = request.headers.get('Authorization')
    type,token = auth.split(" ",1)
    r = autenticacion(username, token)
    if r.status_code == 200:
        ruta = "usuarios/" + username
        data_all = {}
        try:
            ficheros = os.listdir(ruta)
            for fichero in ficheros:
                ruta_doc = ruta + "/" + fichero
                with open(ruta_doc) as datos:
                    fichero = fichero[:-5]
                    data_all[fichero] = json.load(datos)
                    print(data_all[fichero])
            return jsonify(data_all)
        except FileNotFoundError:
            return jsonify({"Error": "Archivo no encontrado "}), 404
    else:
        return jsonify({"Error al autenticar con el usuario": username}), 401
            
def Doc_GET(username, doc_id):
    if request.form.__len__() == 0:
            auth = request.headers.get('Authorization')
    else:
        return jsonify({"Error": "En la entrada de datos"}), 400
    type,token = auth.split(" ",1)
    r = autenticacion(username, token)
    if r.status_code == 200:
        ruta = "usuarios/" + username + "/" + doc_id
        try:
            with open(ruta) as fichero:
                data = json.load(fichero)
                return data
        except FileNotFoundError:
            return jsonify({"Error": "Archivo no encontrado "}), 404
    else:
        return jsonify({"Error al autenticar con el usuario": username}), 401

def Doc_POST(username, doc_id):
    auth = request.headers.get('Authorization')
    contenido = request.get_json().get('doc_content', '')
    type,token = auth.split(" ",1)
    extension = ".json"
    if not extension in doc_id:
        doc_id = doc_id + ".json"
    #return jsonify({"Error": "El archivo debe ser un .json"}), 400
    r = autenticacion(username, token)
    if r.status_code == 200:
        ruta = "usuarios/" + username + "/" + doc_id
        if not os.path.exists("usuarios/"+ username):
                try:
                    os.mkdir("usuarios/" + username)
                except OSError:
                    print("No se ha podido crear el directorio 'usuarios'")
        elif os.path.exists(ruta):
            return jsonify({"Error": "El fichero ya existe, mejor utilizar la funcion PUT"}), 405
        try:
            with open(ruta, 'w') as fichero:
                json.dump(contenido, fichero, indent=4)
                return jsonify({"size": fichero.tell()})
        except FileNotFoundError:
            return jsonify({"Error": "Archivo no encontrado "}), 404
    else:
        return jsonify({"Error al autenticar con el usuario": username}), 401


def Doc_PUT(username, doc_id):
    if request.form.__len__() == 0:
            auth = request.headers.get('Authorization')
            contenido = request.get_json().get('doc_content', '')
    else:
        return jsonify({"Error": "En la entrada de datos"}), 400
    type,token = auth.split(" ",1)
    r = autenticacion(username, token)
    if r.status_code == 200:
        ruta = "usuarios/" + username + "/" + doc_id + ".json"
        if not os.path.exists(ruta):
                return jsonify({"Error": "El documento no existe"}), 404
        try:
            with open(ruta, 'w') as fichero:
                json.dump(contenido, fichero, indent=4)
                return jsonify({"size": fichero.tell()})
        except FileNotFoundError:
            return jsonify({"Error": "Archivo no encontrado "}), 404
    else:
        return jsonify({"Error al autenticar con el usuario": username}), 401
    
def Doc_DELETE(username, doc_id):
    if request.form.__len__() == 0:
            auth = request.headers.get('Authorization')
    else:
        return jsonify({"Error": "En la entrada de datos"}), 400
    type,token = auth.split(" ",1)
    r = autenticacion(username, token)
    if r.status_code == 200:
        ruta = "usuarios/" + username + "/" + doc_id + ".json"
        if os.path.exists(ruta):
                remove(ruta)
                return {}
        else:
            return jsonify({"Error": "Archivo no encontrado "}), 404
    else:
        return jsonify({"Error al autenticar con el usuario": username}), 401

if __name__ == '__main__':
    # __init__()
    context = ('/certificados/files.pem','/certificados/fileskey2.pem') #ruta del certificado y de la key
    app.run(host = '10.0.2.4',debug = True, ssl_context=context)
