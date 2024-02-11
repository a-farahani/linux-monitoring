#!/bin/bash
kill -9 $(ps -aux | grep "python3 -u check-host.py" | grep -v grep | awk -F' ' '{print $2}')