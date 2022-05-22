
protoc -I . --go_out=plugins=grpc:. example.proto
# 或者
protoc -I . --go_out=. --go-grpc_out=. example.proto