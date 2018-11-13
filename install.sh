#!/bin/bash


HX_WALLET_VERSION=1.1.1
CROSSCHAIN_MIDWARE_VERSION=1.0.5


if [ "$1" != "" ]; then
    HX_WALLET_VERSION=$1
fi
if [ "$2" != "" ]; then
    CROSSCHAIN_MIDWARE_VERSION=$2
fi

if [ ! -d "hx" ]; then
    wget https://github.com/HcashOrg/HyperExchange/releases/download/v${HX_WALLET_VERSION}/hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    tar xf hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    mv hx_wallet_linux_v${HX_WALLET_VERSION} hx
    cp third_chain/* hx/
    cp main_chain/start_main_chain.sh hx/
    wget https://github.com/HcashOrg/CrossChainMidWare/releases/download/${CROSSCHAIN_MIDWARE_VERSION}/btc_collect
    wget https://github.com/HcashOrg/CrossChainMidWare/releases/download/${CROSSCHAIN_MIDWARE_VERSION}/eth_collect
    mv btc_collect hx/
    mv eth_collect hx/
    chmod +x hx/*
    wget -O CrossChainMidWare.tar.gz https://github.com/HcashOrg/CrossChainMidWare/archive/${CROSSCHAIN_MIDWARE_VERSION}.tar.gz
    tar xf CrossChainMidWare.tar.gz
    cp main_chain/genesis.json hx/
    mv CrossChainMidWare-${CROSSCHAIN_MIDWARE_VERSION} hx/crosschain_midware
    mkdir -p hx/bitcoin_data hx/hc_data/hcd_data hx/hc_data/hcwallet_data hx/litecoin_data hx/hx_data hx/logs hx/mongo_data
    cp third_chain/starthc.py hx/hc_data/starthc.py
    cp main_chain/collector_conf.py hx/crosschain_midware/btc_data_collector/collector_conf.py
fi

docker-compose up
