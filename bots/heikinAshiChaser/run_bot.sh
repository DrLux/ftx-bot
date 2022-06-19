#!/bin/bash

PLATFORM="arm"

if ! [ "$(ls -A ./externalPackage/)" ] 
then 
    if ! [ "$(ls -A ../../framework/dist/)" ] 
    then 
        cd ../../framework/
        /bin/bash create_wheel.sh
        cd ../bots/heikinAshiChaser/
    fi

    cp ../../framework/dist/*.whl ./externalPackage/ 
fi
    

if [[ $PLATFORM == "pc" ]]
then
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes 
    docker build . -t heikinashichaser --build-arg platform=arm  
    docker run --rm -t -v $PWD:/heikinashichaser  heikinashichaser
    docker run --rm --privileged multiarch/qemu-user-static --reset -p no 
else 
    docker build . -t heikinashichaser --build-arg platform=pc  
    docker run --rm -t -it -v $PWD:/heikinashichaser  heikinashichaser
fi