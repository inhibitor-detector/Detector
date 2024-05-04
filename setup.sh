#!/bin/bash

# apt-get update
# apt-get upgrade -y

# Install deps
apt-get install libusb-1.0
pip install --upgrade pip
pip install watchdog
pip install requests
pip install schedule
pip install python-dotenv

# Install expect tool
apt-get install -y expect

# Install rfcat
git clone https://github.com/atlas0fd00m/rfcat.git
cd rfcat
python3 setup.py install

cd .. #return to /Tesis/app

#clean
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/* /var/tmp/*
