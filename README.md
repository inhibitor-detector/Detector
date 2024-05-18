# Detector

## In this repo

This repo contains all the necesarry software to run the Detector on our "Detector de Inhibidores" Product.

This software is intended to run on each Raspberry Pi that will be used as a detector.

## Setup

1. [Connect via ssh to the RPI.](https://www.raspberrypi.com/documentation/computers/remote-access.html)

2. Download this repo into the RPI
```bash
git pull https://github.com/inhibitor-detector/Detector.git
cd Detector
```

3. Run the setup
```bash
make setup
```
Note: this will download and install:
- [rfcat](https://github.com/atlas0fd00m/rfcat)
- [expect](https://linux.die.net/man/1/expect)
- The necesarry python libraries to make this project work

4. Configure .env
```bash
make generate-env
```
Note: You must then enter the newly created app/.env and configure the environment variables accordingly

## Execution 

To run the software from the RPI, you must:
```bash
make start
```

This will start an [Expect session](./app/auto_rfcat.sh), running a configrued rfcat instance that will print on a file it's output.
Concurrently, this will start a Python program which has various concurrently-running services inside:
- [Main](./app/src/main.py)
  - This is in charge of setting up and running the rest of the services concurrently, as well as verifying some basic input data (if the logs file exists, etc) 
- [Detector](./app/src/models/detector.py)
  - This entity manages the identity of the Detector, as well as its communication with the API, handling the different types of posts, the manage of the JWT token, etc.
- [Analyzer](./app/src/services/analyzer.py)
  - This service is in charge of analyzing the data written into the log. It is the point of communication between the SDR Antenna and the rest of the RPI. It detects normal input data, inhibitor input data, as well as the different possible errors the antenna may have; notifying the Detector of its findings, so the Detector may act accordingly.
- [Heartbeat](./app/src/services/heartbeat.py)
  - This service is in charge of verifying the rest of the services are running (the rfcat and the analyzer). If one or both are not running, it will notify the Detector so he may communicate this information to the API. If everything is running as expected, it will notify the Detector so he may also communicate this information to the API, like a heartbeat. This way, the API will find out if the detector has an internal issue reported by the detector, or will find out if the detector is offline, if it does not recieve the Heartbeat after some time.

Note: this project is currently designed for the RPI to have a [YARD Stick One](https://greatscottgadgets.com/yardstickone/) attached to it, although pretty much any rfcat-compatible SDR should work OK.
