build:
	docker build --rm -f docker/Dockerfile --tag midebian docker/
	docker build --rm -f docker/router/Dockerfile --tag midebian-router docker/router
	docker build --rm -f docker/jump/Dockerfile --tag midebian-jump docker/jump
	docker build --rm -f docker/work/Dockerfile --tag midebian-work docker/work
	docker build --rm -f docker/broker/Dockerfile --tag midebian-broker docker/broker
	docker build --rm -f docker/auth/Dockerfile --tag midebian-auth docker/auth
	docker build --rm -f docker/files/Dockerfile --tag midebian-files docker/files

network:
	-docker network create -d bridge --subnet 10.0.1.0/24 dmz
	-docker network create -d bridge --subnet 10.0.3.0/24 dev
	-docker network create -d bridge --subnet 10.0.2.0/24 srv

containers: build network
	docker run --privileged --rm -ti -d --name router --hostname router midebian-router
	docker network connect dmz router
	docker network connect dev router
	docker network connect srv router

	docker run --privileged --rm -ti -d \
		--name jump --hostname jump --ip 10.0.1.3 --network dmz midebian-jump

	docker run --privileged --rm -ti -d \
		--name broker --hostname broker --ip 10.0.1.4 --network dmz \
		midebian-broker

	docker run --privileged --rm -ti -d \
		--name auth --hostname auth --ip 10.0.2.3 --network srv \
		midebian-auth

	docker run --privileged --rm -ti -d \
		--name files --hostname files --ip 10.0.2.4 --network srv \
		midebian-files

	docker run --privileged --rm -ti -d \
		--name work --hostname work --ip 10.0.3.3 --network dev \
		midebian-work

ssh:
	ssh-add docker/assets/op
	ssh-add docker/assets/dev
#	Comando por si queremos reconocer el nodo work al usar ssh
# 	ssh-keyscan -H 10.0.3.3 >> ~/.ssh/known_hosts

certificado:
	sudo cp docker/broker/certificados/broker.crt /usr/local/share/ca-certificates
	sudo update-ca-certificates
	
remove:
	-docker stop router work jump auth files broker
	-docker network prune -f

clean:
	find . -name "*~" -delete

all: remove clean build network containers
	