#!/bin/bash


HX_WALLET_VERSION=1.0.9


if [ "$1" != "" ]; then
    HX_WALLET_VERSION=$1
fi

if [ ! -d "hx" ]; then
    wget https://github.com/HcashOrg/HyperExchange/releases/download/v${HX_WALLET_VERSION}/hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    tar xf hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    mv hx_wallet_linux_v${HX_WALLET_VERSION} hx
    cp third_chain/* hx/
    cp main_chain/start_main_chain.sh hx/
    chmod +x hx/*
    cp main_chain/genesis.json hx/
    cp -a main_chain/crosschain_midware hx/
    mkdir -p hx/bitcoin_data hx/hc_data/hcd_data hx/hc_data/hcwallet_data hx/litecoin_data hx/hx_data hx/logs hx/mongo_data
    cp third_chain/starthc.py hx/hc_data/starthc.py
fi

docker-compose up
