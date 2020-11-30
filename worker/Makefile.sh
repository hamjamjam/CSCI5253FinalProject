#!/bin/bash
##
## You provide this to build your docker image
##
version=$(git describe)
export PROJECT_ID=ninth-tensor-297101
docker build -t worker:${version} .
docker build -t gcr.io/${PROJECT_ID}/worker:${version} .
docker push gcr.io/${PROJECT_ID}/worker:${version} 
kubectl create deployment worker --image=gcr.io/${PROJECT_ID}/worker:${version}
