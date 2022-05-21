#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# 增加dfinder_py引用
sys.path.append("dfinder_py")

from concurrent import futures
import grpc
import multiprocessing
import os
from dfinder_py.discover.register import Register
from dfinder_py.discover.etcd_conf import EtcdConf
import example_pb2_grpc
import time
import argparse

from example_server import ExampleServerImpl

parser = argparse.ArgumentParser()
parser.add_argument("--etcd_host", type=str, default="127.0.0.1", help="etcd_host (default=127.0.0.1)", required=False)
parser.add_argument("--etcd_port", type=str, default="2379", help="etcd_port (default=2379)", required=False)
parser.add_argument("--addr", type=str, default="127.0.0.1:50051", help="this add server serve addr", required=False)
args = parser.parse_args()


def RegisterNode(servername, addr, env, etcd_conf):
  print(os.getpid())
  print(servername, addr, env)
  r = Register(servername, addr, env, etcd_conf)
  r.Serve()


def Serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers = 4))
  example_pb2_grpc.add_ExampleServiceServicer_to_server(servicer = ExampleServerImpl(), server = server)
  server.add_insecure_port(args.addr)
  server.start()
  print("server start")
  server.wait_for_termination()


def SetUp(env : str, svr : str, addr : str, etcd_conf : EtcdConf):
  register_process = multiprocessing.Process(target = RegisterNode, args = (
    svr,
    addr,
    env,
    etcd_conf
  ))
  serve_process = multiprocessing.Process(target = Serve)

  serve_process.start()
  register_process.start()


if __name__ == '__main__':
  SetUp("dev", "add_server", args.addr, EtcdConf(
    host = args.etcd_host, 
    port = args.etcd_port))
  while True:
    time.sleep(5)
    print("sleep_tag")
    pass