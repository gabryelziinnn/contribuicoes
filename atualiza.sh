#!/usr/bin/env bash
awk -F '["]' '/RouteTableId/{ print $4 }' info.txt 1>> output.txt
awk -F '["]' '/SubnetId/{ print $4 }' info.txt 1>> output.txt
awk -F '["]' '/InternetGatewayId/{ print $4 }' info.txt 1>> output.txt
cat vpc_id.txt | awk -F'[%]' '{print $1}' 1>> output.txt


