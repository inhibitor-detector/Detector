#!/usr/bin/bash

filename="log_$(date +'%Y-%m-%d_%H-%M-%S').txt"
touch "./logs/$filename"

./auto_rfcat.sh | tee "./logs/$filename" #tee allows to write to a file but also show in STO
