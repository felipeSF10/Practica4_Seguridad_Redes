# PRACTICA 4. SEGURIDAD EN REDES
URL del proyecto en Github https://github.com/felipeSF10/Practica4_Seguridad_Redes
## Autores
🔹 Miguel Ángel Roldán Mora <br>
🔹 Felipe Segovia Friginal

## Pasos para iniciar el entorno
Antes de comenzar debemos de situarnos dentro de la carpeta demo-ssh.
### "make certificado"
Como primer paso debemos copiar el certificado del nodo broker en nuestro sistema para poder utilizar el protocolo https.
### "make all"
Iniciaremos el entorno de practicas realizando el comando 'make all' el cual realizara un build de los diferentes docker, un network para la configuración de la red del sistema distribuido y un container para la inicialización de los contenedores.
### "make ssh"
Con el cual copiamos las claves privadas de dev y de op a nuestro ssh-agent.
Podemos realizar el comando "ssh-keyscan -H 10.0.3.3 >> ~/.ssh/known_hosts" para que reconozcamos al nodo work al realizar ssh.

## Entorno de pruebas API-REST
Para realizar las pruebas automáticas de las funcionalidades básicas de la API ejecutaremos el comando "./test.py".
Tambien le facilitamos comandos CURL para realizar pruebas manualmente.
La ip que se utilizan en los comando CURL y en el test.py es la ip pública del router del sistema(172.17.0.2), ya que este se encarga de nodo de conexión entre el exterior y el sistema interno API-REST.
### Comandos CURL
A la hora de realizar los comandos curl es necesario primero iniciar sesión (login), es posible cambiar el contenido de usuario, contraseña, el token y el doc_Content
que mostramos en las pruebas.
#### Version
curl -X GET https://172.17.0.2:5000/version
#### Signup
curl -X POST -H "Content-Type: application/json" -d '{"username":"Felipe2","password":"Prueba1"}' https://172.17.0.2:5000/signup
#### Login
curl -X POST -H "Content-Type: application/json" -d '{"username":"Felipe","password":"Prueba1"}'  https://172.17.0.2:5000/login
#### POST DOC
curl -X POST -H "Authorization: token 955c1ca9-09ac-4527-ba21-273374de305b" -H "Content-Type: application/json" -d '{"doc_Content":{"asd":"asdda"}}' https://172.17.0.2:5000/Felipe/coches2.json
#### GET DOC
curl -X GET -H "Authorization: token 955c1ca9-09ac-4527-ba21-273374de305b" https://172.17.0.2:5000/Felipe/moto.json
#### GET ALL DOCS
curl -X GET -H "Authorization: token 955c1ca9-09ac-4527-ba21-273374de305b" https://172.17.0.2:5000/Felipe/_all_docs
#### PUT DOC
curl -X PUT -H "Authorization: token 955c1ca9-09ac-4527-ba21-273374de305b" -H "Content-Type: application/json" -d '{"doc_Content":{"123":"12345"}}' https://172.17.0.2:5000/Felipe/coches2.json
#### DELETE DOC
curl -X DELETE -H "Authorization: token 955c1ca9-09ac-4527-ba21-273374de305b" https://172.17.0.2:5000/Felipe/coches2.json

## Comunicación SSH
Para la comunicación ssh destacar que se trata de 3 usuarios diferentes: 
🔸 Jump que se utiliza unicamente para iniciar el primer salto desde el exterior al sistema mediante el nodo JUMP. <br>
🔸 Dev se trata de un usuario sin privilegios que solo puede entrar al nodo Work atraves del nodo de salto JUMP. <br>
🔸 Op se trata de un usuario con privilegios y al contrario que dev puede entrar a todos los nodos unicamente entrando primero al nodo WORK atraves del nodo de salto JUMP. <br>
### Ejemplo SSH
Mediante el comando "ssh -J jump@172.17.0.2 -A op@10.0.3.3" podemos entrar al nodo WORK mediante el nodo de salto JUMP con el usuario OP. Con "-J jump@172.17.0.2" utilizamos el usuario jump como intermediario para entrar al nodo de salto JUMP desde fuera de la red del sistema y con el comando "-A op@10.0.3.3" entramos al usuario op con su clave privada para poder conectarnos al nodo WORK. <br>
Estando dentro del nodo WORK con el usuario OP podremos hacer conexion ssh a cualquier otro nodo. Como ejemplo hacemos ssh al nodo broker: "ssh op@10.0.1.4".

## Configuración de la red
### Red DMZ 10.0.1.0/24
* Default Gateway 10.0.1.2 
* Interfaz de Red eth1 
* JUMP 10.0.1.3 
* BROKER 10.0.1.4
### Red SRV 10.0.2.0/24
* Default Gateway 10.0.2.2 
* Interfaz de Red eth3
* AUTH 10.0.2.3 
* FILES 10.0.2.4
### Red SRV 10.0.3.0/24
* Default Gateway 10.0.3.2 
* Interfaz de Red eth2
* WORK 10.0.3.3 

## File2ban
Se ha configurado un sistema de file2ban con un máximo de 3 intentos y un tiempo de baneo de IP de 600s para evitar ataques de fuerza bruta a la comunicacion ssh de nuestro sistema.



