# 云服务器搭建jupyter notebook服务

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

