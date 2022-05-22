package main

import (
	"flag"
	"log"
	"net"

	"github.com/dxyinme/dfinder-example/go/example"
	"github.com/dxyinme/dfinder-example/go/svr"
	"github.com/dxyinme/dfinder-go/discover"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

func Register(svrname, addr, env, etcd_addr string) {
	etcd_conf := discover.DefaultEtcdCfg
	etcd_conf.Endpoints = []string{etcd_addr}
	r, err := discover.NewRegisterWithEtcdCfg(svrname, addr, env, etcd_conf)
	if err != nil {
		logrus.Error(err)
	}
	go r.Serve()
}

func main() {
	addr := flag.String("addr", "0.0.0.0:50022", "addr")
	etcd_addr := flag.String("etcd_addr", "127.0.0.1:2379", "etcd addr")
	svrname := flag.String("svrname", "testname1", "svr name")
	flag.Parse()
	lis, err := net.Listen("tcp", *addr)
	if err != nil {
		logrus.Fatal(err)
	}
	s := grpc.NewServer()
	example_svr := &svr.ExampleSvr{}
	example.RegisterExampleServiceServer(s, example_svr)
	Register(*svrname, *addr, "dev", *etcd_addr)
	if err = s.Serve(lis); err != nil {
		log.Fatal(err)
	}
}
