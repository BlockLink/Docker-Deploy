#!/bin/bash
init_flag=0
if [ ! -d "/var/formal_data/postgresql_data" ]; then
    mkdir -p /var/formal_data/postgresql_data
    chown -R postgres /var/formal_data/postgresql_data
    su postgres -c "/usr/lib/postgresql/10/bin/initdb -D /var/formal_data/postgresql_data"
    init_flag=1
fi
su postgres -c "/usr/lib/postgresql/10/bin/postgres -D /var/formal_data/postgresql_data >logfile 2>&1 &"
sleep 5
if [ $init_flag -eq 1 ]; then
    su postgres -c "/usr/lib/postgresql/10/bin/createdb eth_db"
    su postgres -c "/usr/lib/postgresql/10/bin/psql eth_db -f /hx/crosschain_midware/init_eth_db.sql"
fi
mongod --dbpath /hx/mongo_data --bind_ip_all --port 27017 >> /hx/logs/mongod_file 2>&1 &
sleep 10
mongo --port 27017 --quiet /hx/crosschain_midware/mgmt/init_db.js
/hx/btc_collect -ChainType=BTC >> /hx/logs/btc_collect_file 2>&1 &
/hx/btc_collect -ChainType=LTC >> /hx/logs/ltc_collect_file 2>&1 &
/hx/btc_collect -ChainType=HC >> /hx/logs/hc_collect_file 2>&1 &
/hx/eth_collect -ChainType=ETH >> /hx/logs/eth_collect_file 2>&1 &

pip install gunicorn

gunicorn -w 4 -b 127.0.0.1:5010 --chdir /hx/crosschain_midware -D --log-file /hx/logs/app_file_gunicorn --error-logfile /hx/logs/app_file_error_gunicorn app:app

# python /hx/crosschain_midware/app.py 5006 >> /hx/logs/app_file1 2>&1 &
# python /hx/crosschain_midware/app.py 5007 >> /hx/logs/app_file2 2>&1 &
# python /hx/crosschain_midware/app.py 5008 >> /hx/logs/app_file3 2>&1 &
# python /hx/crosschain_midware/app.py 5009 >> /hx/logs/app_file4 2>&1 &

apt install -y nginx
cp /hx/main_chain_nginx_conf /etc/nginx/sites-available/default
service nginx restart

/hx/hx_node --data-dir=/hx/hx_data --rpc-endpoint=0.0.0.0:8090 --p2p-endpoint=0.0.0.0:9034 >> /hx/logs/witness_file 2>&1 &
screen -dmS hx /hx/hx_client --rpc-http-endpoint=0.0.0.0:8093 
sleep 20
python /hx/crosschain_midware/btc_data_collector/run_server.py bk >> /hx/logs/hx_collect_file 2>&1 &
python /hx/crosschain_midware/btc_data_collector/run_server.py hc >> /hx/logs/hc_python_collect_file 2>&1 &
python /hx/crosschain_midware/btc_data_collector/run_server.py ltc >> /hx/logs/ltc_python_collect_file 2>&1 &
python /hx/crosschain_midware/btc_data_collector/run_server.py btc >> /hx/logs/btc_python_collect_file 2>&1 &
python /hx/crosschain_midware/omni_data_collector/omni_data_collector/run_server.py usdt >> /hx/logs/usdt_python_collect_file 2>&1 &
python /hx/crosschain_midware/eth_data_collector/run_server.py  >> /hx/logs/eth_python_collect_file 2>&1 &
/bin/bash
