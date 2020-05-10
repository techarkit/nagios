#!/bin/bash
## Created Date: 27th Sep 2016
## Author: Ankam Ravi Kumar
## Web Site: https://arkit.co.in
## Purpose: To Generate Nagios Configuration files within minute of time.
## Usage Explanation: https://arkit.co.in/generate-nagios-configuration-using-shell-script/

mkdir temp-cfg
cat  nagios-windows.csv | while read LINE
do
    HostIP=`echo $LINE | cut -d, -f1`
    HostName=`echo $LINE | cut -d, -f2`
    sed -e "s/XXXX/$HostName/g; s/ZZZZ/$HostIP/g" Nagios-Template-Linux.cfg > temp-cfg/$HostName.cfg
done
