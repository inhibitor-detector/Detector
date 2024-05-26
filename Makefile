setup:
	./setup.sh

run:
	./start.sh

stop:
	./stop.sh
	
generate-env:
	cp ./app/.env.example ./app/.env