.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./start.sh

stop:
	./stop.sh
	
generate-env:
	cp ./app/.env.example ./app/.env