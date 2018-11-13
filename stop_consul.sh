#!/bin/bash
consul_pid=`ps -au | grep "consul agent" | grep -v "grep" | awk '{ print $2 }'`
kill $consul_pid
echo "killing $consul_pid"
