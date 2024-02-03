#!/bin/bash
cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate
nohup python3 -u check-host.py &
