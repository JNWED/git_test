#!/bin/bash
echo "Stop the severs which only works at Linux/Mac"
kill $(ps -ax |grep "appium" |grep -v grep| awk '{print $1}')
kill $(lsof -t -i:8886)
