from flask import Flask, jsonify
from flask import request
import json
import requests

#Creamos la API con Flask
app = Flask(__name__)
app.secret_key = "broker"
VERSION = "2.0.1"
URL_AUTH = "https://10.0.2.3:5000"  #URL del autenticator
URL_FILES = "https://10.0.2.4:5000"     #URL de Files

#Metodo para hacer los requests al autenticator o a files
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
        if r.status_code != 200:    #Si el estado de la peticion es diferente a 200, devolvemos el mensaje de error que nos ha devuelto el autenticator
            error_message = json.loads(r.text)  #obtiene el mensaje de la peticion
            return jsonify({"Error" : error_message["Error"]}), r.status_code
        return jsonify(r.json())

class SignUp():
    @app.route('/signup', methods = ['POST'])#ruta de la funcion
    def Signup_POST():
        user = request.get_json().get('username','')
        passw = request.get_json().get('password', '')
        r = _req("signup", URL_AUTH, data={"username": user, "password": passw}, method="POST", verify='/certificados/auth.pem')
        print("Respuesta de Authenticator: ",r.status_code)
        if r.status_code != 200:
            error_message = json.loads(r.text)
            return jsonify({"Error" : error_message["Error"]}), r.status_code
        return jsonify(r.json())

class ExploradorDocumentos():
    @app.route('/<string:username>/<string:doc_id>', methods = ['GET', 'POST', 'PUT', 'DELETE'])#ruta de la funcion
    def ExploradorDoc(username, doc_id):
        #user = request.get_json().get('username','')
        auth = request.headers.get('Authorization')
        type,token = auth.split(" ",1)
        if request.method == 'POST' or request.method == 'PUT':
            contenido = request.get_json().get('doc_content', '')
            r = _req(f"{username}/{doc_id}", URL_FILES, data={"doc_content": contenido}, method=request.method, verify='/certificados/files.pem', token=token)
        else:
            r = _req(f"{username}/{doc_id}", URL_FILES, method=request.method, verify='/certificados/files.pem', token=token) #Peticiones GET, GET_ALL_DOCS y DELETE como tienen la misma estructura
        if r.status_code != 200:
            error_message = json.loads(r.text)
            return jsonify({"Error" : error_message["Error"]}), r.status_code #Devuelve el mensaje erroneo devuelto en la peticion y el estado de la peticion
        return jsonify(r.json())
        

if __name__ == '__main__':
    # __init__()
    context = ('certificados/broker.crt','certificados/brokerkey2.key') #ruta del certificado y de la key
    app.run(host = '10.0.1.4',debug = True, ssl_context=context)