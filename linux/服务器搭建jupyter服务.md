# 一、 云服务器搭建jupyter notebook服务

## 1. 下载安装anaconda

手动下载：

官网：https://repo.continuum.io/archive/

清华源下载地址：https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/

下载后安装（以Ubuntu18.04 x86-64）为例：

```
# 创建anaconda存放文件夹
mkdir anaconda
# 进入该文件夹
cd anaconda
# 如果是手动下载则直接上传至该文件夹
# 使用wget下载anaconda安装包
wget https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh
# 安装anaconda
bash Anaconda3-2019.10-Linux-x86_64.sh
```

安装完成后通过source激活环境变量。

## 2. 配置jupyter notebook

首先，生成jupyter notebook的配置文件

```
# 生成配置文件
jupyter notebook --generate-config
# 如果需要用户权限加上--allow-root
jupyter notebook --allow-root --generate-config
```

打开配置文件进行修改，添加如下字段，注意工作文件夹需要事先创建好：

```
c.NotebookApp.ip='*'
c.NotebookApp.password = u'此处填写密码'
c.NotebookApp.open_browser = False
c.NotebookApp.port =8888
c.NotebookApp.notebook_dir = '/home/ubuntu/py3jupyterproject/'
```

## 3. 运行服务

直接运行jupyter notebook即可，如果未设置密码则会随机生成一个token，复制链接到本地的浏览器访问即可远程使用服务器测试代码啦！

# 二、云服务器中使用docker镜像管理jupyter notebook服务

很显然，上述方法是非常繁琐复杂，且不容易维护的，因此推荐使用jupyter notebook的官方镜像进行搭建。

## 1. 拉取jupyter notebook的docker镜像

官方的镜像应该都是基于ubuntu LTS 18.04

* 基于数据分析的jupyter镜像

```
docker pull jupyter/datascience-notebook
```

* 基于tensorflow的jupyter镜像

```
docker pull jupyter/tensorflow-notebook
```

更多镜像可以进入[dockerhub](hub.docker.com)的jupyter官方[jupyter](https://hub.docker.com/u/jupyter)或[jupyterhub](https://hub.docker.com/u/jupyterhub)进行检索。

## 2. 启动jupyter notebook的镜像

以后台运行的方式启动jupyter镜像，并映射宿主机端口8888：

```
docker run -d -p 8888:8888 --name=jupyter jupyter/scipy-notebook
```

## 3. 进入运行的容器，设置jupyter密码

这里提供一种简易的模式进行jupyter密码配置，如果需要进行详细配置请参考[这里](https://blog.csdn.net/ys676623/article/details/77848427)

```
docker exec -it jupyter /bin/bash
```

以伪终端的方式进入jupyter容器内部后，可以查看容器中的各种包，使用方法与ubuntu相同。但是sudo命令需要jovyan用户的密码。目前无法使用vim。

终端输入：

```
jupyter notebook password
```

输入两次密码，即可设置完成

## 4. 服务器内安装pip包推荐使用不缓存和清华源拉取

```
!pip install --no-cache-dir tensorflow==2.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

 