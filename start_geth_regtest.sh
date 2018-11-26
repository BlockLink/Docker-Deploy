#!/bin/bash 

if [! -d "./hx/geth_bin" ]; then 
    wget https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.8.18-58632d44.tar.gz -O ./hx/geth_bin.tar.gz
    tar -xzf ./hx/geth_bin.tar.gz -C ./hx/
    mv ./hx/geth-linux-amd64-1.8.18-58632d44/ ./hx/geth_bin
fi

if [ ! -d "./hx/eth_regtest_data" ]; then
    ./hx/geth_bin/geth --datadir ./hx/eth_regtest_data init ./geth_regtest_genesis.json 
    ./hx/geth_bin/geth --datadir ./hx/eth_regtest_data account new
fi
./hx/geth_bin/geth --networkid 314590  --datadir ./hx/eth_regtest_data --rpcapi net,admin,eth,miner,web3,personal --rpc --port 10700 --rpcaddr 0.0.0.0 --rpcport 60015 --rpcvhosts eth_wallet --verbosity 2 --mine --minerthreads=2 console
