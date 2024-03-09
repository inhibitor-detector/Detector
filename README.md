# Tesis

## In this repo

A Dockerfile that makes a Docker image with RFCat and its necesarry dependencies. And when executed, it will automatically run `rfcat` to analyze the traffic on the frequency 433.92 MHz

To build this docker image, with output image name rfcat_container_1, we must:
```bash
sudo docker build -t rfcat_container_1 .
```

## Execution 
As we want to run it using YARD Stick One, we must redirect its usb input to the inside of the Docker container, like this:

First you must run on your pc the following command, and identify YARD's usb ID
```bash
lsusb
```
An example output of this could be:
```
uri@PEPE:/dev$ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 004: ID 04f2:b57e Chicony Electronics Co., Ltd EasyCamera
Bus 001 Device 017: ID 1d50:605b OpenMoko, Inc. RfCat YARD Stick One
Bus 001 Device 009: ID 0c45:5004 Microdia Redragon Mitra RGB Keyboard
Bus 001 Device 005: ID 0bda:0821 Realtek Semiconductor Corp. RTL8821A Bluetooth
Bus 001 Device 002: ID 046d:c08b Logitech, Inc. G502 SE HERO Gaming Mouse
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Here, we can identify YARD Stick One on Bus 001, Device 017.

Then, we can run our docker image using `docker run` as follows:

```bash
sudo docker run -it --privileged --device=/dev/bus/usb/001/017 rfcat_container_1
```
Note the flags: 
- `-it`:
    - `i` interactive, which allows us to interact with the container by providing input.
    - `t` terminal, which allocates a pseudo-TTY (teletypewriter) to the container, enabling you to see its output and interact with it as if it were a local terminal.
- `--privileged`: to run the image with privilages, needed to run rfcat inside without using "sudo", which is not configured out of the box for docker containers(?)
- `--device=/dev/bus/usb/001/017`: to use our usb device inside the docker container


## Debugging
For debugging, we can acces directly inside the container by running the following:
```bash
sudo docker run -it --privileged --device=/dev/bus/usb/001/017 --entrypoint /bin/bash rfcat_container_1
```
Note the new flag: 
- `--entrypoint /bin/bash`: to execute a shell inside our container, temporarily bypassing the `CMD` line from our Dockerfile

Now, we have access to our docker container. From within it we can run, for example, the following to start a `research`, interactive, mode for rfcat.
```bash
rfcat -r
```