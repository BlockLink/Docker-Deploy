#!/bin/bash
mongod --dbpath /hx/mongo_data --bind_ip_all --port 27017 >> /hx/logs/mongod_file 2>&1 &
sleep 10
mongo --port 27017 --quiet /hx/crosschain_midware/mgmt/init_db.js
python /hx/crosschain_midware/btc_data_collector/run_server.py btc >> /hx/logs/btc_collect_file 2>&1 &
python /hx/crosschain_midware/btc_data_collector/run_server.py ltc >> /hx/logs/ltc_collect_file 2>&1 &
python /hx/crosschain_midware/btc_data_collector/run_server.py hc >> /hx/logs/hc_collect_file 2>&1 &
python /hx/crosschain_midware/app.py >> /hx/logs/app_file 2>&1 &
/hx/hx_node --data-dir=/hx/hx_data --rpc-endpoint 0.0.0.0:8090 --p2p-endpoint 0.0.0.0:9034 >> /hx/logs/witness_file 2>&1 
