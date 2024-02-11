#!/bin/bash
tag=$1
docker push alirezaf75/check-host:$tag
docker push alirezaf75/check-host:latest
