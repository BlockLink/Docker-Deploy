#!/usr/bin/python
# coding: utf-8

from __future__ import print_function
import os
import sys
import json
import tempfile
import time


class ProcessInfo(object):
    def __init__(self, uid, pid, cpu, mem, vsz, rss, tty, stat, start, create_time, cmd):
        self.uid = uid
        self.pid = pid
        self.cpu = cpu
        self.mem = mem
        self.vsz = vsz
        self.rss = rss
        self.tty = tty
        self.stat = stat
        self.start = start
        self.create_time = create_time
        self.cmd = cmd

    def __str__(self):
        d = {
            'uid': self.uid,
            'pid': self.pid,
            'cpu': self.cpu,
            'mem': self.mem,
            'vsz': self.vsz,
            'rss': self.rss,
            'tty': self.tty,
            'stat': self.stat,
            'start': self.start,
            'create_time': self.create_time,
            'cmd': self.cmd,
        }
        return json.dumps(d)


def list_processes_in_docker(container_key):
    try:
        if container_key is not None and container_key != '' and container_key != 'host':
            docker_ps = os.popen('docker exec %s ps -aux' % str(container_key)).read()
        else:
            docker_ps = os.popen("ps -aux").read()
        lines = docker_ps.split('\n')
        if len(lines) < 1:
            raise Exception('invalid response of docker top %s' % str(container_key))
        result = []
        for line in lines[1:]:
            if len(line.strip()) < 1:
                continue
            splited = line.split(None, 10)
            if len(splited) < 11:
                raise Exception("invalid process info of %s" % line)
            uid, pid, cpu, mem, vsz, rss, tty, stat, start, create_time, cmd = splited
            info = ProcessInfo(uid, pid, cpu, mem, vsz, rss, tty, stat, start, create_time, cmd)
            result.append(info)
        return result
    except Exception as e:
        print("list_processes_in_docker error: ", e)
        return None

def get_collector1_block_height(container_key, http_port):
    try:
        if container_key is not None and container_key != '' and container_key != 'host':
            output = os.popen('docker exec %s curl -s --header "Content-Type: application/json" --request POST --data \'{"method":"Service.GetBlockHeight","id":1,"params":[]}\' http://127.0.0.1:%d' % (str(container_key), int(http_port))).read()
        else:
            output = os.popen('curl -s --header "Content-Type: application/json" --request POST --data \'{"method":"Service.GetBlockHeight","id":1,"params":[]}\' http://127.0.0.1:%d' % int(http_port)).read()
        result = json.loads(output)
        height = result.get('result', None)
        if height is None:
            raise Exception("response %s" % str(output))
        return int(height)
    except Exception as e:
        print("get_collector1_block_height error: ", e)
        return None

def ProcessFilter(cmd):
    def f(info):
        if info is None or cmd is None:
            return False
        info_cmd = info.cmd
        if info_cmd is None: return False
        if cmd in info_cmd:
            return True
        else:
            return False
    return f

needed_processed = {
    'BTC1': '/hx/btc_collect -ChainType=BTC',
    'BTC2': 'python /hx/crosschain_midware/btc_data_collector/run_server.py btc',
    'LTC1': '/hx/btc_collect -ChainType=LTC',
    'LTC2': 'python /hx/crosschain_midware/btc_data_collector/run_server.py ltc',
    'HC1': '/hx/btc_collect -ChainType=HC',
    'HC2': 'python /hx/crosschain_midware/btc_data_collector/run_server.py hc',
    'ETH1': '/hx/eth_collect -ChainType=ETH',
    'ETH2': 'python /hx/crosschain_midware/eth_data_collector/run_server.py',
    'bitcoind': '/hx/bitcoind',
    'hcd': '/hx/hcd',
    'hcwallet': '/hx/hcwallet',
    'litecoind': '/hx/litecoind',
    'geth': 'geth',
}

# first-level collector's http rpc port
process_collector1_config = {
    'BTC1': {'port': 5444, 'max_height_not_change_seconds': 30*60,},
    'LTC1': {'port': 5445, 'max_height_not_change_seconds': 10*60,},
    'HC1': {'port': 5447, 'max_height_not_change_seconds': 10*60},
}

def get_collector1_block_height_cache_file(container_key, process_type):
    return "%s/cache_collector1_block_height_container_%s_process_%s" % (tempfile.tempdir or '/tmp', container_key, process_type)

def get_cache_of_collector1_block_height(container_key, process_type):
    """read cache of collector1's last collected block height"""
    cpath = get_collector1_block_height_cache_file(container_key, process_type)
    if not os.path.isfile(cpath):
        return None
    try:
        cache_txt = open(cpath).read()
        cache = json.loads(cache_txt)
        return cache
    except Exception as e:
        print("read cache error: ", e)
        return None

def cache_collector1_block_height(container_key, process_type, height):
    """update cache of collector1's last collected block height"""
    cpath = get_collector1_block_height_cache_file(container_key, process_type)
    try:
        if not os.path.isfile(cpath):
            cache = {}
        else:
            cache_txt = open(cpath).read()
            cache = json.loads(cache_txt)
        cache['last_block_height'] = height
        cache["last_time"] = int(time.time())
        with open(cpath, 'w') as f:
            f.write(json.dumps(cache))
    except Exception as e:
        print("set cache error: ", e)
        return    

def main():
    argv = sys.argv
    keys = list(needed_processed.keys())
    if len(argv) < 3 or argv[1] == '-h':
        print("need pass container key(or 'host') and process name as arguments, available processes are: %s" % ', '.join(keys))
        sys.exit(1)
        return
    container_key = argv[1]
    for process_type in argv[2:]:
        if process_type not in keys:
            print("not allowed process name %s" % process_type)
            sys.exit(1)
            return
        process_cmd = needed_processed[process_type]
        processes = list_processes_in_docker(container_key)
        if processes is None:
            print("error happened")
            sys.exit(1)
            return
        cmd_processes = list(filter(ProcessFilter(process_cmd), processes))
        if len(cmd_processes) <= 0:
            print("cmd %s not active now" % process_cmd)
            sys.exit(1)
            return
        print(str(cmd_processes[0]))
        collector1_conf = process_collector1_config.get(process_type, None)
        if collector1_conf is not None:
            block_height = get_collector1_block_height(container_key, collector1_conf['port'])
            if block_height is None:
                sys.exit(1)
                return
            max_height_not_change_seconds = collector1_conf['max_height_not_change_seconds']
            cache = get_cache_of_collector1_block_height(container_key, process_type)
            if cache is not None:
                last_block_height = cache['last_block_height']
                last_time = cache['last_time']
                if block_height == last_block_height:
                    now = int(time.time())
                    if (now - last_time) > max_height_not_change_seconds:
                        print("too long time not collected now block height")
                        sys.exit(1)
                        return
                else:
                    cache_collector1_block_height(container_key, process_type, block_height)
            else:
                cache_collector1_block_height(container_key, process_type, block_height)
            print("container %s service %s's block height is %d" % (container_key, process_type, block_height))

if __name__ == '__main__':
    main()

