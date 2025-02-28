.PHONY: setup start stop generate-env logs

setup:
	./setup.sh

start:
	./supervisor.sh > output.log 2>&1 &
	@echo "Starting..."
	@echo "You can now run 'make logs' to view the logs in real time"

logs:
        @tail -f -n+0 output.log

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