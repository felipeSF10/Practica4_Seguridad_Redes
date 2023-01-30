from flask import Flask, jsonify
import os
# from os import remove
from flask import request
import hashlib
from uuid import uuid4
from threading import *
# import json

#Creamos la API con Flask
app = Flask(__name__)
app.secret_key = "10.0.2.3"

TIEMPO = 300

#diccionario donde guardamos el usuario y su token correspondiente
diccionario_tokens = {}

#Metodo para borrar el token cuando pasa el tiempo de espera
def refreshAuthorization(usuario):
    a = diccionario_tokens.pop(usuario)
    print(f"{usuario}: token borrado ({a})")

#Metodo para comprobar que los argumentos sean correctos
def validarUsuarioYContrasena(usuario, contrasena):
    error=""
    if not usuario.isalnum():
        error = "El usuario no puede contener caracteres especiales. "
    if len(contrasena) < 6  :
        error = error + "Contrasena muy corta, debe tener minimo 6 caracteres. "
    else:
        minuscula = False
        mayuscula = False
        for minus in contrasena:
            if minus.islower()==True:
                minuscula=True
        if not minuscula:
            error = error + "La contrasena debe tener al menos una minuscula. "
        for mayus in contrasena:
            if mayus.isupper()==True:
                mayuscula=True
        if not mayuscula:
            error = error + "La contrasena debe tener al menos una mayuscula."   
    return error

def existeUsuario(usuario, file):
    existe = False
    registros = file.readlines()
    for reg in registros:
        if usuario in reg:
            existe = True
            return existe
    return existe

def comprobarInicioSesion(usuario, hash, file):
    coincide = False
    registros = file.readlines()
    for reg in registros:
        if usuario in reg:
            if hash in reg:
                coincide = True
                return coincide
    return coincide

class SignUp():
    @app.route('/signup', methods = ['POST'])#ruta de la funcion
    def SignUp_POST():
        print("+++ Testing /signup... ")
        usuario = request.get_json().get('username','')
        contrasena = request.get_json().get('password', '')
        err = validarUsuarioYContrasena(usuario, contrasena)
        if err != "":
            return jsonify({'Error al registrar': err}), 400
        try:
            file = open(".shadow", mode = '+r')
        except FileNotFoundError:
            with open(".shadow", "w") as shadow_file:
                shadow_file.write("")
            file = open(".shadow", mode = '+r')

        if not existeUsuario(usuario, file):
            hash = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
            registro = (f"{usuario} : {hash}\n") 
            file.write(registro)
            access_token = str(uuid4())
            file.close()
            diccionario_tokens[usuario] = access_token
            t = Timer(TIEMPO, refreshAuthorization, [usuario])
            t.start()
            if not os.path.exists("usuarios/"+ usuario):
                try:
                    os.mkdir("usuarios/" + usuario)
                except OSError:
                    print("No se ha podido crear el directorio 'usuarios'")
        else:
            file.close()
            return jsonify({"Error": "El nombre de usuario ya existe"}), 409

        return jsonify({'access_token': access_token})

class Login():
    @app.route('/login', methods = ['POST'])#ruta de la funcion
    def Login_POST():
        usuario = request.get_json().get('username','')
        print(usuario)
        contrasena = request.get_json().get('password', '')
        print(contrasena)
        try:
            file = open(".shadow", mode = '+r')
        except FileNotFoundError:
            with open(".shadow", "w") as shadow_file:
                shadow_file.write("")
            file = open(".shadow", mode = '+r')

        hash = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
        if comprobarInicioSesion(usuario, hash, file):
            access_token = str(uuid4())
            file.close()
            diccionario_tokens[usuario] = access_token
            t = Timer(TIEMPO, refreshAuthorization, [usuario])
            t.start()         
        else:
            file.close()
            return jsonify({"Error": "La contrasena o el usuario es incorrecto"}), 401
        return jsonify({'access_token': access_token})

class Autenticar():
    @app.route('/autenticar', methods = ['POST'])#ruta de la funcion
    def Autenticar_POST():
        usuario = request.get_json().get('username','')
        auth = request.headers.get('Authorization')
        type,token = auth.split(" ",1)
        if usuario in diccionario_tokens:
            if diccionario_tokens[usuario] == token:
                return {}, 200
        return jsonify({"Error": "La contrasena o el usuario es incorrecto"}), 401

    
if __name__ == '__main__':
    # __init__()
    context = ('/certificados/auth.pem','/certificados/authkey2.pem') #ruta del certificado y de la key
    app.run(host = '10.0.2.3',debug = True, ssl_context=context)
