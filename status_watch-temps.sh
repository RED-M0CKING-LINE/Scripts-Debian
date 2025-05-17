#!/bin/bash

# This script is a shorthand to read the temprature of a system into the console and keep it updated
echo 'Must install lm-sensors for this program to work! (this displays every time)'


watch -n 2 sensors
