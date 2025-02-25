.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./supervisor.sh &

stop:
	./stop.sh

stop_supervisor:
	kill -9 $$(pgrep -f supervisor)

stop_all:
	$(MAKE) stop_supervisor
	$(MAKE) stop

restart:
	./stop.sh
	./start.sh
	
generate-env:
	cp ./app/.env.example ./app/.env