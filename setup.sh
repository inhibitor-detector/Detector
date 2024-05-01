#!/bin/bash

apt-get update
apt-get upgrade -y

# Install deps
apt-get install libusb-1.0
pip install --upgrade pip

# Install expect tool
apt-get install -y expect

# Install Repo
git clone https://github.com/uri-99/Tesis.git
cd Tesis/app

# Install rfcat
git clone https://github.com/atlas0fd00m/rfcat.git
cd rfcat
python3 setup.py install

cd .. #return to /Tesis/app


apt-get autoremove -y
apt-get clean
# worked in docker, check in .sh
# rm -rf /var/lib/apt/lists/*
# rm -rf /tmp/* /var/tmp/*

# Run rfcat on start
./start.sh
