#!/usr/bin/env bash
sudo docker build -t classis .
sudo docker run -d -p 8080:5000 classis
