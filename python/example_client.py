#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# 增加dfinder_py引用
sys.path.append("dfinder_py")

import time
import example_pb2_grpc
import example_pb2
import grpc
import argparse
from dfinder_py.discover.discover import Discover
from dfinder_py.discover.etcd_conf import EtcdConf

parser = argparse.ArgumentParser()
parser.add_argument("--etcd_host", type=str, default="127.0.0.1", help="etcd_host (default=127.0.0.1)", required=False)
parser.add_argument("--etcd_port", type=str, default="2379", help="etcd_port (default=2379)", required=False)
args = parser.parse_args()


if __name__ == '__main__':
  dco = Discover("dev", EtcdConf(host = args.etcd_host, port = args.etcd_port))
  while True:
    addr = dco.GetRandomAddr("add_server")
    print(addr)
    c = grpc.insecure_channel(addr)
    stub = example_pb2_grpc.ExampleServiceStub(c)
    resp = stub.Add(example_pb2.AddReq(a = 1, b = 2))
    print(resp)
    time.sleep(5)