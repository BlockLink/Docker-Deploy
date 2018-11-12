#!/usr/bin/python
# coding: utf-8

from __future__ import print_function
import os
import sys
import json


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
        cmd_processes = list(filter(ProcessFilter(process_cmd), processes))
        if len(cmd_processes) <= 0:
            print("cmd %s not active now" % process_cmd)
            sys.exit(1)
            return
        print(str(cmd_processes[0]))

if __name__ == '__main__':
    main()

