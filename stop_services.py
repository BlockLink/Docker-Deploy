#!/usr/bin/python
from __future__ import print_function
import os
import sys
import time

def try_parse_int(s):
  if not s or s == '':
    return None
  try:
    return int(s)
  except Exception as e:
    return None

def fetch_service_pid(container_key, cmd):
  output = os.popen("docker exec %s ps -au | grep \"%s\" | grep -v \"grep\" | awk '{ print $2 }'" % (container_key, cmd)).read()
  return try_parse_int(output)

main_chain_key = "main_chain"
third_chain_key = "third_chain"

def get_collector_pids():
  return {
    'btc_collector1': fetch_service_pid(main_chain_key, "btc_collect -ChainType=BTC"),
    'ltc_collector1': fetch_service_pid(main_chain_key, "btc_collect -ChainType=LTC"),
    'hc_collector1': fetch_service_pid(main_chain_key, "btc_collect -ChainType=HC"),
    'eth_collector1': fetch_service_pid(main_chain_key, "eth_collect -ChainType=ETH"),
    'btc_collector2': fetch_service_pid(main_chain_key, "run_server.py btc"),
    'ltc_collector2': fetch_service_pid(main_chain_key, "run_server.py ltc"),
    'hc_collector2': fetch_service_pid(main_chain_key, "run_server.py hc"),
    'eth_collector2': fetch_service_pid(main_chain_key, "eth_data_collector/run_server.py"),
  }

def kill_service_gracefully(container_key, pid):
  if not container_key or container_key == '' or container_key == 'host':
    os.system('kill %d' % pid)
  else:
    os.system("docker exec %s kill %d" % (container_key, pid))

def kill_chain_wallet_service_gracefully(wallet_name):
  wallet_name = wallet_name.strip().lower()
  configs = {
    "btc": { 'host': '127.0.0.1', 'port': 60011, },
    "ltc": { 'host': '127.0.0.1', 'port': 60012, },
    "hcwallet": { "host": "127.0.0.1", 'port': 19021, },
    "hcd": { 'host': '127.0.0.1', 'port': 19019, },
  }
  if wallet_name == 'btc':
    config = configs[wallet_name]
    output = os.popen("""curl -s -X POST   http://%s:%d/   -H 'authorization: Basic YTpi'   -H 'content-type: application/json'   -d '{
 "id": 1, "method": "stop", "params": []}'""" % (config['host'], config['port'])).read()
    return output
  elif wallet_name == 'ltc':
    config = configs[wallet_name]
    output = os.popen("""curl -s -X POST   http://%s:%d/   -H 'authorization: Basic YTpi'   -H 'content-type: application/json'   -d '{ "id": 1, "method": "stop", "params": []'}""" % (config['host'], config['port'])).read()
    return output
  elif wallet_name == 'hc':
    config1 = configs['hcwallet']
    config2 = configs['hcd']
    cmd1 = "curl -s -X POST   http://%s:%d/   -H 'authorization: Basic YTpi'   -H 'content-type: application/json' -d '{ \"id\": 1,\"method\": \"stop\", \"params\": []}'" % (config1['host'], config1['port'])
    output1 = os.popen(cmd1).read()
    output2 = os.popen("docker exec %s curl -s -X POST   http://%s:%d/   -H 'authorization: Basic YTpi'   -H 'content-type: application/json'   -d '{ \"id\": 1, \"method\": \"stop\", \"params\": []}'" % (third_chain_key, config2['host'], config2['port'])).read()
    return output1 + '\n' + output2
  else:
    print("not support wallet name %s, available wallet names are: btc/ltc/hc" % wallet_name)
    sys.exit(1)

def main():
  option = 'list'
  argv = sys.argv
  if len(argv) < 2:
    option = 'list'
  elif argv[1] == '-h':
    option = 'help'
  else:
    option = argv[1]
  if option == 'help':
    print("""available options: list, -h, help, all, collectors2, collectors1, wallets, geth, btc, ltc, hc""")
    return
  all_collectors = get_collector_pids()
  if option == "list":
    print(all_collectors)
  elif option == "all":
    for k in ['btc_collector2', 'ltc_collector2', 'hc_collector2', 'eth_collector2']:              
      pid = all_collectors.get(k, None)                                                            
      if pid:                                                                                      
        kill_service_gracefully(main_chain_key, pid)                                               
        print("sent kill to %s, please wait some seconds and then list services" % k)              
    for k in ['btc_collector1', 'ltc_collector1', 'hc_collector1', 'eth_collector1']:                      
       pid = all_collectors.get(k, None)                                                                    
       if pid:                                                                                              
         kill_service_gracefully(main_chain_key, pid)                                                       
         print("sent kill to %s, please wait some seconds and then list services" % k)                      
    output = kill_chain_wallet_service_gracefully('btc')                    
    print(output)                                                           
    output = kill_chain_wallet_service_gracefully('ltc')                    
    print(output)                                                           
    output = kill_chain_wallet_service_gracefully('hc')                     
    print(output)                                                           
  elif option == "collectors2":
    for k in ['btc_collector2', 'ltc_collector2', 'hc_collector2', 'eth_collector2']:
      pid = all_collectors.get(k, None)
      if pid:
        kill_service_gracefully(main_chain_key, pid)
        print("sent kill to %s, please wait some seconds and then list services" % k)
  elif option == "collectors1":
     for k in ['btc_collector1', 'ltc_collector1', 'hc_collector1', 'eth_collector1']:     
       pid = all_collectors.get(k, None)                                                   
       if pid:                                                                             
         kill_service_gracefully(main_chain_key, pid)                                      
         print("sent kill to %s, please wait some seconds and then list services" % k)  
  elif option == "wallets":
    output = kill_chain_wallet_service_gracefully('btc')
    print(output)
    output = kill_chain_wallet_service_gracefully('ltc')
    print(output)
    output = kill_chain_wallet_service_gracefully('hc')  
    print(output)
  elif option == "btc":
    output = kill_chain_wallet_service_gracefully('btc')     
    print(output)       
  elif option == "ltc":                                   
    output = kill_chain_wallet_service_gracefully('ltc')  
    print(output)  
  elif option == "hc":                                   
    output = kill_chain_wallet_service_gracefully('hc')  
    print(output)                                                                                                                     
  elif option == "geth":
    print("TODO")
    sys.exit(1)
  else:
    print("unknown option, please use -h to see help")
    sys.exit(1)

if __name__ == '__main__':
  main()
