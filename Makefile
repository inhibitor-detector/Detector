.PHONY: setup start stop generate-env

setup:
	./setup.sh

start:
	./supervisor.sh &

stop:
	./stop.sh

stop_supervisor:
	@if pgrep -f supervisor > /dev/null; then \
		kill -9 $$(pgrep -f supervisor); \
	else \
		echo "No supervisor process found."; \
	fi

stop_all: stop_supervisor
	$(MAKE) stop

restart:
	./stop.sh
	./start.sh
	
generate-env:
	cp ./app/.env.example ./app/.env