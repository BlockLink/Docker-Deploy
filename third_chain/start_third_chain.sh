#!/bin/bash

cp /hx/third_chain_nginx_conf /etc/nginx/sites-available/default
service nginx restart

/hx/bitcoind   -testnet -datadir=/hx/bitcoin_data -testnet  -rpcuser=a -rpcpassword=b -rpcallowip=0.0.0.0/0 -rpcport=60011 -server  -txindex &
/hx/hcd --appdata /hx/hc_data/hcd_data -u a -P b --notls --rpclisten 127.0.0.1:19019 --testnet --whitelist 127.0.0.1/24 --txindex setgenerate true --miningaddr TsVtYhsRxZ1xynRajBqfHP5uvpWFNC5sSHQ &
python /hx/hc_data/starthc.py &
sleep 15
/hx/hcwallet -A /hx/hc_data/hcwallet_data -u a -P b --testnet --pass 12345678 -c 127.0.0.1:19019 --noclienttls --rpclisten :19020 --rpccert=/hx/hc_data/hcwallet_data/rpc.cert  --debuglevel warn &
/hx/litecoind  -testnet -datadir=/hx/litecoin_data -testnet -rpcuser=a -rpcpassword=b -rpcallowip=0.0.0.0/0 -rpcport=60012 -server  -txindex

