#!/bin/bash

sudo apt update

# Install
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv my-venv
# pip install -r requirements.txt into virtual env
my-venv/bin/pip install -r requirements.txt
