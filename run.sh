#!/bin/bash

source venv/bin/activate

python3 main.py > logfile.txt 2>&1

deactivate
