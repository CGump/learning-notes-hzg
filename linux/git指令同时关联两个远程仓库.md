# git指令同时关联两个远程仓库

## 1. 首先查看当前本地仓库的远程关联情况
```
git remote -v
```
此时显示
```
origin  http://10.2.11.226/iot-7/fruit/GY191208.git (fetch)
origin  http://10.2.11.226/iot-7/fruit/GY191208.git (push)
```
表明默认的origin远程仓库关联的是自建gitlab库，如果此时为空的话，需要先进行默认关联后再查看：
```
git remote add origin http://10.2.11.226/iot-7/fruit/GY191208.git
git remote -v
```

## 2. 通过`add`方法添加另一个远程仓库
再使用`add`方法进行另一个远程仓库的添加，注意此时另一个远程仓库不能再用origin名称，需要另起一个名字，以github为例：
```
git remote add cgump  https://github.com/CGump/my-Food-identification-network.git
git remote -v
```
## 3. 再次查看关联情况
此时查看就可以看到已经关联了两个远程仓库
```
cgump   https://github.com/CGump/my-Food-identification-network.git (fetch)
cgump   https://github.com/CGump/my-Food-identification-network.git (push)
origin  http://10.2.11.226/iot-7/fruit/GY191208.git (fetch)
origin  http://10.2.11.226/iot-7/fruit/GY191208.git (push)
```
然后再使用相应的命令`pull`或`push`就可以进行远程的拉取和推送操作。缺点是每次需要`push`两次。
```
git pull name
git push -u name master
```

## 4. 方法二，只需要`push`一次：使用`git remote set-url`命令
* 删除方法一的cgump仓库
```
git remote rm cgump
```
* 使用如下命令添加远程仓库
```
git remote set-url --add origin https://github.com/CGump/my-Food-identification-network.git
```
* 查看远程仓库情况，可以看到gitlab的远程仓库有两个push地址，这种方法只需要push一次就行了
```
git remote -v
git push -u origin master
```
