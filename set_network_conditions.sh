#!/bin/bash

# Set network conditions
set_conditions() {
    sudo tc qdisc add dev eth0 root handle 1: htb default 12
    sudo tc class add dev eth0 parent 1: classid 1:1 htb rate $1
    sudo tc qdisc add dev eth0 parent 1:1 handle 10: netem delay $2 loss $3
}

# Remove network conditions
remove_conditions() {
    sudo tc qdisc del dev eth0 root
}

# Example usage
case $1 in
    set)
        set_conditions $2 $3 $4
        ;;
    remove)
        remove_conditions
        ;;
    *)
        echo "Usage: $0 {set|remove} [rate] [delay] [loss]"
        ;;
esac
