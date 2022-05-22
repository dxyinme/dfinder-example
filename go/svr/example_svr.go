package svr

import (
	"context"

	"github.com/dxyinme/dfinder-example/go/example"
	"github.com/sirupsen/logrus"
)

type ExampleSvr struct {
	example.UnimplementedExampleServiceServer
}

func (es *ExampleSvr) Add(ctx context.Context, req *example.AddReq) (*example.AddRsp, error) {
	logrus.Infof("a=%d,b=%d", req.A, req.B)
	return &example.AddRsp{
		Res:           req.A + req.B,
		ServerMessage: "go-dfinder-example",
	}, nil
}
