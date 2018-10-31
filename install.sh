#!/bin/bash


HX_WALLET_VERSION=1.0.9


if [ "$1" != "" ]; then
    HX_WALLET_VERSION=$1
fi

if [ ! -d "hx" ]; then
    wget https://github.com/HcashOrg/HyperExchange/releases/download/v${HX_WALLET_VERSION}/hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    tar xf hx_wallet_linux_v${HX_WALLET_VERSION}.tar.gz
    mv hx_wallet_linux_v${HX_WALLET_VERSION} hx
    cp hx/hx_node main_chain/
fi

docker-compose up
