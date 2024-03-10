#!/usr/bin/bash

filename="file_$(date +'%Y-%m-%d_%H-%M-%S').txt"
touch "./logs/$filename"

./auto_rfcat.sh > "./logs/$filename"
