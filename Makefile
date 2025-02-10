.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./start_supervisor.sh

stop:
	./stop.sh

restart:
	./stop.sh
	./start.sh
	
generate-env:
	cp ./app/.env.example ./app/.env