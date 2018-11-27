#!/bin/bash

if [! -d "./hx/geth_bin" ]; then
    wget https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.8.18-58632d44.tar.gz -O ./hx/geth_bin.tar.gz
    tar -xzf ./hx/geth_bin.tar.gz -C ./hx/
    mv ./hx/geth-linux-amd64-1.8.18-58632d44/ ./hx/geth_bin
fi

./hx/geth_bin/geth --networkid 15  --datadir ./hx/eth_testnet_data --rpcapi net,admin,eth,miner,web3,personal --rpc --port 10700 --rpcaddr 0.0.0.0 --rpcport 60015 --rpcvhosts eth_wallet console
