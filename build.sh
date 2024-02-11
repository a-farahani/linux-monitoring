#!/bin/bash
tag=$1
docker build -t alirezaf75/check-host:$tag .
docker tag alirezaf75/check-host:$tag alirezaf75/check-host:latest

