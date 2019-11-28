# docker操作指南

```
构建
docker build -f Dockerfile-base -t fruit:v1.0 .
运行
docker run -d -p 17061:17061 --name=fruit  fruit:v1.0
查看运行的docker
docker container ls -all
删除原有
docker container rm fruit
查看运行状态
docker ps
docker ps -a
查看运行日志
docker logs -f fruit
停止服务
docker stop fruit
```

