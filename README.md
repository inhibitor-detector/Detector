# Detector

## In this repo

This repo contains the necesarry software to run the "Detector de Inhibidores" Product.

This repo must be git pulled by each Raspberry Pi used as a detector.

## Setup

Connect via ssh to the RPI.

Get this repo into the RPI
```
git pull
```

Run the setup script
```
./setup.sh
```
Note: this will install x things

## Execution 

```
./start.sh
```

This will start an Expect session, running a rfcat that will print on a file the output.
Concurrently, this will start an analyzer that will read this file and decide if an inhibitor appeared. If so, it will post the necesarry information to the API of this project.
