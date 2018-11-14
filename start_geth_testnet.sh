#!/bin/bash
geth --networkid 15  --datadir ../eth_testnet_data --rpcapi net,admin,eth,miner,web3,personal --rpc --port 10700 --rpcaddr 0.0.0.0 --rpcport 60015 --rpcvhosts eth_wallet console
