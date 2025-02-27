.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./supervisor.sh >> supervisor.log 2>&1 &

stop:
	./stop.sh

stop_supervisor:
	kill -9 $$(pgrep -f supervisor)

stop_all:
	kill -9 $$(pgrep -f supervisor) &
	./stop.sh

restart:
	./stop.sh
	./start.sh
	
generate-env:
	cp ./app/.env.example ./app/.env