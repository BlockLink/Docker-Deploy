#!/bin/bash
./consul agent -dev -config-dir=./consul.d  >> ./hx/logs/consul_log 2>&1 &
sleep 5
curl --request PUT --data @consul_services/collector.json http://127.0.0.1:8500/v1/agent/service/register
curl --request PUT --data @consul_services/chain_wallets.json http://127.0.0.1:8500/v1/agent/service/register
curl --request PUT --data @consul_services/geth.json http://127.0.0.1:8500/v1/agent/service/register
echo "registered consul services"

