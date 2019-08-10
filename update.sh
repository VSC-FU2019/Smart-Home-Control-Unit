#!/bin/bash

git pull
sudo systemctl restart doreamon.service
sudo systemctl restart config_wifi.service

