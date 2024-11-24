#!/bin/bash

# Update the package list
sudo apt update

# Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv qtwayland5

#pip install -r requirements.txt
python3 -m venv my-venv

my-venv/bin/pip install -r requirements.txt
