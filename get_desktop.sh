#!/bin/bash
# Author: Eshan Roy

set -e

DESKTOP="UNKNOWN"

function detect_awesome(){
    ps -e | grep -E '^.* awesome$' > /dev/null
    if [ $? -ne 0 ];
    then
        return 0
    fi
    VERSION=$(awesome --version | head -1 | awk '{print $2}')
    DESKTOP="AWESOME"
    return 1
}

function detect_bspwm(){
    ps -e | grep -E '^.* bspwm$' > /dev/null
    if [ $? -ne 0 ];
    then
        return 0
    fi
    VERSION=$(bspwm -v | head -1 | awk '{print $1}')
    DESKTOP="BSPWM"
    return 1
}

# echo DESKTOP