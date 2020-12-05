#!/bin/bash
img_file="${1:-'eggs,salt,finelychoppedonion,milk,butter,shreddedSwisscheese,slicesbacon,all-purposeflour'}"
IP=$(kubectl get services | grep ^rest | awk '{print $4}')
python3 rest-client.py ${IP}:5000 ingredients "${img_file}" 1
# https://static.toiimg.com/photo/msid-68523832/68523832.jpg 1
