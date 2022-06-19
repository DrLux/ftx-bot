#!/bin/bash

PLATFORM="arm"

if [[ $PLATFORM == "arm" ]]
then
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes 
    docker build . -t builderframework --build-arg platform=arm  
    docker run --rm -it -t -v $PWD:/framework  builderframework
    docker run --rm --privileged multiarch/qemu-user-static --reset -p no 
else
    docker build . -t builderframework --build-arg platform=pc  
    docker run --rm -it -t -v $PWD:/framework  builderframework
fi