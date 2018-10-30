#!/usr/bin/env python
# encoding: utf-8
import subprocess
import os
import time
import sys

def start():
    exist = os.path.isfile(r"/hx/hc_data/hcwallet_data/rpc.cert")
    if not exist:
        filePath1 = '/hx/hcwallet -A "/hx/hc_data/hcwallet_data" -u "a" -P "b" --testnet -c "127.0.0.1:19019" --noclienttls --rpclisten "192.168.18.6:19020" --create'
        filePath2 = '/hx/hcwallet -A "/hx/hc_data/hcwallet_data" --pass 12345678 -u "a" -P "b" --testnet -c "127.0.0.1:19019" --noclienttls --rpclisten "192.168.18.6:19020"'
        child1 = subprocess.Popen(filePath1, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr, shell=True)
        child1.stdin.write("12345678\n")
        child1.stdin.flush()
        child1.stdin.write("12345678\n")
        child1.stdin.flush()
        child1.stdin.write("no\n")
        child1.stdin.flush()
        child1.stdin.write("no\n")
        child1.stdin.flush()
        child1.stdin.write("OK\n")
        child1.stdin.flush()
        time.sleep(10)
        child2 = subprocess.Popen(filePath2, stdin=subprocess.PIPE, stdout=sys.stdout, stderr=sys.stderr, shell=True)
        time.sleep(5)
        child2.kill()
    else:
        print "exist file,no need to create"

if __name__ == '__main__':
    #aa()
    start()
