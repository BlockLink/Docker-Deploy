#!/bin/bash


HX_WALLET_VERSION=1.1.1
CROSSCHAIN_MIDWARE_VERSION=1.0.6


if [ "$1" != "" ]; then
    HX_WALLET_VERSION=$1
fi
if [ "$2" != "" ]; then
    CROSSCHAIN_MIDWARE_VERSION=$2
fi

if [ ! -d "hx" ]; then
    wget https://github.com/HcashOrg/HyperExchange/releases/download/v${HX_WALLET_VERSION}/hx_wallet_linux_${HX_WALLET_VERSION}.tar.gz
    tar xf hx_wallet_linux_${HX_WALLET_VERSION}.tar.gz
    mv hx_${HX_WALLET_VERSION} hx
    cp third_chain/* hx/
    cp third_chain/start_third_chain_testnet.sh hx/start_third_chain.sh
    cp third_chain/starthc_testnet.py hx/starthc.py
    cp main_chain/start_main_chain.sh hx/
    cp main_chain/query_collector2.js hx/

    wget https://github.com/HcashOrg/CrossChainMidWare/releases/download/${CROSSCHAIN_MIDWARE_VERSION}/btc_collect
    wget https://github.com/HcashOrg/CrossChainMidWare/releases/download/${CROSSCHAIN_MIDWARE_VERSION}/eth_collect
    mv btc_collect hx/
    mv eth_collect hx/
    chmod +x hx/*
    git clone https://github.com/HcashOrg/CrossChainMidWare.git CrossChainMidWare
    cp main_chain/genesis.json hx/
    mv CrossChainMidWare hx/crosschain_midware
    mkdir -p hx/bitcoin_data hx/hc_data/hcd_data hx/hc_data/hcwallet_data hx/litecoin_data hx/hx_data hx/logs hx/mongo_data
    cp third_chain/starthc_testnet.py hx/hc_data/starthc.py
    cp main_chain/collector_conf.py hx/crosschain_midware/btc_data_collector/collector_conf.py
    cp main_chain/init_db_testnet.js hx/crosschain_midware/mgmt/init_db.js
fi

source ./set_env.sh
docker-compose -f docker-compose-testnet.yml up -d