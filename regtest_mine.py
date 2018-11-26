#!/usr/bin/python3
# coding: utf-8
from __future__ import print_function
import os
import sys
import time
import threading

def get_btc_newaddress():
  out = os.popen('./bitcoin-cli -rpcport=60011 -rpcuser=a -rpcpassword=b getnewaddress ""').read()
  return out

def mine_btc_cycle(addr):
  while True:
    os.popen('./bitcoin-cli -rpcport=60011 -rpcuser=a -rpcpassword=b generatetoaddress 1000 %s' % addr).read()
    time.sleep(600)

def get_btc_blockcount():
  out = os.popen('./bitcoin-cli -rpcport=60011 -rpcuser=a -rpcpassword=b getblockcount').read()
  return int(out)


def get_ltc_newaddress():
  out = os.popen('./litecoin-cli -rpcport=60012 -rpcuser=a -rpcpassword=b getnewaddress ""').read()
  return out

def mine_ltc_cycle(addr):
  while True:
    os.popen('./litecoin-cli -rpcport=60012 -rpcuser=a -rpcpassword=b generatetoaddress 1000 %s' % addr).read()
    time.sleep(600)

def get_ltc_blockcount():
  out = os.popen('./litecoin-cli -rpcport=60012 -rpcuser=a -rpcpassword=b getblockcount').read()
  return int(out)

def main():
  btc_blockcount = get_btc_blockcount()
  print("current btc blockcount: ", btc_blockcount)
  btc_addr = get_btc_newaddress()
  print("mine to btc address ", btc_addr)
  t1 = threading.Thread(target=mine_btc_cycle, args=(btc_addr,))
  t1.start()

  
  ltc_blockcount = get_ltc_blockcount()
  print("current ltc blockcount: ", ltc_blockcount)
  ltc_addr = get_ltc_newaddress()
  print("mine to ltc address ", ltc_addr)
  t2 = threading.Thread(target=mine_ltc_cycle, args=(ltc_addr,))
  t2.start()
  while True:
    time.sleep(1)

if __name__ == '__main__':
  main()
