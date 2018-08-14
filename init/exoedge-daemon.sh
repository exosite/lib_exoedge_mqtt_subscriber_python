#!/bin/bash

# SysV init script for exoedge

NAME="exoedge-daemon"
LOCK="/var/lock/$NAME"
ENABLED="yes"

MURANO_HOSTNAME=https://h34u57agngaa00000.m2.exosite.io/
MURANO_PORT=443
DEBUG_LEVEL=WARNING

run_dir=/var/run/exoedge
conf_dir=/var/config/exoedge
conf_file=$conf_dir/exoedge-daemon.conf
config_io_file=$conf_dir/exoedge-daemon.json

exoedge_daemon=/usr/bin/edged
exoedge_daemon_log=/var/log/exoedge.log
exoedge_daemon_pidfile=$run_dir/$NAME.pid

do_start() {
    # create run directory
    mkdir -p $run_dir/1
    rm -rf $run_dir/1/*

    echo -n "Starting $NAME: "
    # start network server
     start-stop-daemon \
        --start \
        --background \
        --make-pidfile \
        --pidfile $exoedge_daemon_pidfile \
        --startas /bin/bash \
        -- \
        -c "exec $exoedge_daemon \
        --host ${MURANO_HOSTNAME} \
        --port ${MURANO_PORT} \
        --debug ${DEBUG_LEVEL} \
        --ini-file $conf_file \
        --config-io-file $config_io_file \
        --local-strategy \
        >> $exoedge_daemon_log 2>&1"
    sleep 2
    # start packet forwarder
    /usr/sbin/start-stop-daemon \
        --chdir $run_dir/1 \
        --background \
        --start \
        --make-pidfile \
        --pidfile $pkt_fwd_pidfile \
        --startas /bin/bash \
        -- -c "exec $pkt_fwd &>$pkt_fwd_log"

    echo "OK"
}

do_stop() {
    echo -n "Stopping $NAME: "
    start-stop-daemon \
        --stop \
        --quiet \
        --oknodo \
        --pidfile $exoedge_daemon_pidfile \
        --retry TERM/60/KILL/5
    start-stop-daemon \
        --stop \
        --quiet \
        --oknodo \
        --pidfile $pkt_fwd_pidfile \
        --retry 5
    rm -f $exoedge_daemon_pidfile $pkt_fwd_pidfile
    echo "OK"
}

if [ "$ENABLED" != "yes" ]; then
    echo "$NAME: disabled in /etc/default"
    exit
fi

force_stop() {
    do_stop
    rm -fr $LOCK
}

function try_lock() {
    if mkdir $LOCK; then
        trap "rm -fr $LOCK" EXIT
    else
        echo "ExoEdge Daemon lock not acquired, resource in use."
        exit 1
    fi
}

case "$1" in
    "start")
            try_lock
            do_start
        ;;
    "stop")
            force_stop
        ;;
    "restart")
            ## Stop the service and regardless of whether it was
            ## running or not, start it again.
            try_lock
            do_stop
            do_start
        ;;
    *)
            ## If no parameters are given, print which are avaiable.
            echo "Usage: $0 {start|stop|restart}"
            exit 1
    ;;
esac

[]