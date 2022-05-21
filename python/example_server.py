#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import example_pb2
import example_pb2_grpc

class ExampleServerImpl(example_pb2_grpc.ExampleServiceServicer):
  def __init__(self) -> None:
    pass

  def Add(self, request : example_pb2.AddReq, context) -> example_pb2.AddRsp:
    print(request.a, request.b)
    return example_pb2.AddRsp(
      res = request.a + request.b,
      server_message = "python-dfinder-example"
    )