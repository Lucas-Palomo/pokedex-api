#!/bin/bash

pip3 install -r requirements.txt
python3 src/main.py collect --limit --limit-size 50 # Testing only # prod disable this flags
python3 src/main.py migrate
python3 src/main.py start