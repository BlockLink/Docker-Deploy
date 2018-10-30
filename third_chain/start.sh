#!/bin/bash
bitcoind   -testnet -datadir=/hx/bitcoin_data   -rpcuser=a -rpcpassword=b -rpcallowip=192.168.0.0/16 -rpcport=60011 -server  -txindex &
hcd --appdata /hx/hc_data/hcd_data -u a -P b --notls --rpclisten 127.0.0.1:19019 --testnet --whitelist 127.0.0.1/24 --txindex setgenerate true --miningaddr TsVtYhsRxZ1xynRajBqfHP5uvpWFNC5sSHQ &
python /hx/hc_data/starthc.py &
sleep 15
hcwallet -A /hx/hc_data/hcwallet_data -u a -P b --testnet --pass 12345678 -c 127.0.0.1:19019 --noclienttls --rpclisten :19020 --rpccert=/hx/hc_data/hcwallet_data/rpc.cert  --debuglevel warn &
litecoind  -testnet -datadir=/hx/litecoin_data  -rpcuser=a -rpcpassword=b -rpcallowip=192.168.0.0/16 -rpcport=60012 -server  -txindexa