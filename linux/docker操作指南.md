# docker操作指南

## 一、docker安装

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口。

### 1. 卸载旧版本

由于Ubuntu里apt官方库里的docker版本可能比较低，因此先用下面的命令行卸载旧版本（如果有的话）：

```
sudo apt-get remove docker docker-engine docker-ce docker.io
```

终端打印信息：

```
(base) ubuntu@VM-0-3-ubuntu:~$ sudo apt-get remove docker docker-engine docker-ce docker.io
Reading package lists... Done
Building dependency tree
Reading state information... Done
Package 'docker-engine' is not installed, so not removed
Package 'docker-ce' is not installed, so not removed
Package 'docker' is not installed, so not removed
Package 'docker.io' is not installed, so not removed
0 upgraded, 0 newly installed, 0 to remove and 126 not upgraded.
```

### 2. 更新apt包索引

```
sudo apt-get update
```

终端打印信息：

```
Hit:1 http://mirrors.tencentyun.com/ubuntu bionic InRelease
Get:2 http://mirrors.tencentyun.com/ubuntu bionic-security InRelease [88.7 kB]
Get:3 http://mirrors.tencentyun.com/ubuntu bionic-updates InRelease [88.7 kB]
Fetched 177 kB in 0s (369 kB/s)
Reading package lists... Done
```

### 3. 调整HTTPS协议

```
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
```

### 4. 添加docker官方提供的GPG秘钥

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
阿里源：
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

### 5. 设置stable存储库

```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
阿里源：
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```

再次更新apt包索引：

```
sudo apt-get update
```

### 6. 安装最新版本的docker-ce

```
sudo apt-get install -y docker-ce
```

### 7. 安装完毕

安装完成后，运行`ps -aux`可以查看docker进程为

```
root     27724  0.0  7.6 757088 77224 ?        Ssl  15:30   0:00 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

使用命令`sudo docker version`可以查看安装docker的版本：

```
(base) ubuntu@VM-0-3-ubuntu:~$ sudo docker version
Client: Docker Engine - Community
 Version:           19.03.5
 API version:       1.40
 Go version:        go1.12.12
 Git commit:        633a0ea838
 Built:             Wed Nov 13 07:29:52 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.5
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.12
  Git commit:       633a0ea838
  Built:            Wed Nov 13 07:28:22 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683

```

使用命令`sudo docker run hello-world`，能观察到从远程下载这个测试用的容器：Pulling from library/hello-world:

然后看到打印消息：Hello from Docker! 说明Docker安装成功。

```
(base) ubuntu@VM-0-3-ubuntu:~$ sudo docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:4fe721ccc2e8dc7362278a29dc660d833570ec2682f4e4194f4ee23e415e1064
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 8. 安装nvidia-docker2

* 添加静态GPG密钥：

  ```bash
  distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
     && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
     && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
  ```

  如果此使报告找不到有效的 OpenPGP 数据，多半是因为这个github.io的域名问题，打开https://github.io.ipaddress.com/网址，输入https://nvidia.github.io/nvidia-docker/gpgkey查询该网址的ip可以看到：

  ```
  185.199.108.153 nvidia.github.io
  185.199.109.153 nvidia.github.io
  185.199.110.153 nvidia.github.io
  185.199.111.153 nvidia.github.io
  ```

  此时将上述信息复制到`/etc/hosts`文件尾端可以看到如下内容：

  ```bash
  $ cat /etc/hosts
  127.0.0.1       localhost
  127.0.1.1       ubuntu-desktop
  185.199.108.153 nvidia.github.io
  185.199.109.153 nvidia.github.io
  185.199.110.153 nvidia.github.io
  185.199.111.153 nvidia.github.io
  
  # The following lines are desirable for IPv6 capable hosts
  ::1     ip6-localhost ip6-loopback
  fe00::0 ip6-localnet
  ff00::0 ip6-mcastprefix
  ff02::1 ip6-allnodes
  ff02::2 ip6-allrouters
  ```

  再次运行就可以了
  
* 更新apt-get
  
```bash
  sudo apt-get update
  ```
  
* 安装nvidia-docker2

  ```
  sudo apt-get install -y nvidia-docker2
  ```

* 重新启动docker以加载nvidia-docker2配置

  ```bash
  sudo systemctl restart docker
  ```

* 运行示例以检查nvidia-docker2是否安装成功

  ```bash
  sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
  ```

  成功的话显示如下信息：

  ```bash
  Unable to find image 'nvidia/cuda:11.0-base' locally
  11.0-base: Pulling from nvidia/cuda
  54ee1f796a1e: Pull complete
  f7bfea53ad12: Pull complete
  46d371e02073: Pull complete
  b66c17bbf772: Pull complete
  3642f1a6dfb3: Pull complete
  e5ce55b8b4b9: Pull complete
  155bc0332b0a: Pull complete
  Digest: sha256:774ca3d612de15213102c2dbbba55df44dc5cf9870ca2be6c6e9c627fa63d67a
  Status: Downloaded newer image for nvidia/cuda:11.0-base
  Mon Mar 22 07:52:21 2021
  +-----------------------------------------------------------------------------+
  | NVIDIA-SMI 450.102.04   Driver Version: 450.102.04   CUDA Version: 11.0     |
  |-------------------------------+----------------------+----------------------+
  | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
  |                               |                      |               MIG M. |
  |===============================+======================+======================|
  |   0  TITAN RTX           Off  | 00000000:3B:00.0  On |                  N/A |
  | 41%   33C    P8    23W / 280W |    947MiB / 24217MiB |      4%      Default |
  |                               |                      |                  N/A |
  +-------------------------------+----------------------+----------------------+
  
  +-----------------------------------------------------------------------------+
  | Processes:                                                                  |
  |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
  |        ID   ID                                                   Usage      |
  |=============================================================================|
  +-----------------------------------------------------------------------------+
  ```

  

## 二. docker基础操作
### 1. 常用指令
* 构建
```
docker build -f Dockerfile-base -t fruit:v1.0-alpha .
```
* 运行
```
docker run -d -p 17061:17061 --name=fruit  fruit:v1.0-alpha
```
* 查看运行的docker
```
docker container ls -all
```
* 删除原有
```
docker container rm fruit
```
* 查看运行状态
```
docker ps
docker ps -a
```
* 停止服务
```
docker stop fruit
```

* 删除Exited状态的docker 容器（container）

```
docker rm $(docker ps -a | grep Exited | awk '{print $1}')
```

* 删除docker镜像（image）

```
docker rmi [iamge/imageID]
docker image rm [image/iamgeID]
```

### 2. 进入正在运行的docker容器

* 进入正在运行的docker

```
docker exec -it fruit /bin/sh
```

* 退出正在运行的docker，并保持运行

```
Ctrl + P + Q
```

### 3. 查看docker的日志

docker运行日志通过以下命令查看

```
docker logs -f fruit
```
## 三、 本地镜像管理
### 1. docker build命令

**docker build **命令用于使用Dockerfile创建镜像。

语法：

```
docker build [OPTIONS] PATH | URL | -
```

docker常用的OPTIONS说明：

* `-if`：指定要使用的dockerfile路径

* `-t, -tag`：镜像的名字及标签，通常以name：tag或者name格式；在一次构建中为一个镜像设置多个标签。
## 四、容器生命周期管理
### 1. docker run命令

**docker run **命令用于创建一个新的容器，并运行一个命令

语法：

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

* `-i`：以交互模式运行容器，通常与 -t 同时使用；
* `-t`：为容器重新分配一个伪输入终端，通常与 -i 同时使用；
* `-it`：为`-i`和`-t`的组合命令，以交互模式运行容器并分配一个伪输入终端；
* `-d`：后台运行容器，并返回容器ID，一般后跟`镜像名：版本`；
* `-p`： 指定端口映射，格式为：`主机(宿主)端口:容器端口`；
* `--name=[name]`： 为容器指定一个名称；
* `--rm`：容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 `docker rm` 。对于调试容器，不需要排障和保留结果，因此使用 `--rm` 可以避免浪费空间。  

### 2. docker start/stop/restart 命令

**docker start**：启动一个或多个已经被停止的容器

**docker stop**：停止一个运行中的容器

**docker restart**：重启容器

语法：

```
docker start [OPTIONS] CONTAINER [CONTAINER...]
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker restart [OPTIONS] CONTAINER [CONTAINER...]
```

### 3. docker exec命令

**docker exec** 命令用于在运行中的容器执行命令

语法：

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

* `-d`：分离模式: 在后台运行；
* `-i`：即使没有附加也保持STDIN 打开；
* `-t`：分配一个伪终端。

例如进入一个正在运行容器内的bash命令行：

```
docker exec -it [name] /bin/bash
docker exec -it [ID] /bin/bash
```




## 五、容器操作

### 1. docker ps命令

**docker ps**命令用于列出当前所有的docker容器。

语法：

```
docker ps [OPTIONS]
```

* `-a`显示所有的容器，包括未运行的。

* `-f`：根据条件过滤显示的内容。

* `--format`：指定返回值的模板文件。

* `-l`：显示最近创建的容器。

* `-n`：列出最近创建的n个容器。

* `--no-trunc`：不截断输出。

* `-q`：静默模式，只显示容器编号。

* `-s`：显示总的文件大小。

## 六、一些有意思的docker镜像

### 1. jupyter notebook官方镜像

```
docker pull jupyter/datascience-notebook
```

2