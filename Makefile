.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./supervisor.sh

stop:
	./stop.sh

stop_supervisor:
	pgrep -f supervisor | kill -9

restart:
	./stop.sh
	./start.sh
	
generate-env:
	cp ./app/.env.example ./app/.env