# git 操作指南

## 1. git全局配置
```
git config --global user.name "黄智刚"
git config --global user.email "560201@gree.com.cn"
```
## 2. 新建一个代码仓库
```
git clone http://10.2.11.226/iot-7/fruit/gree-fruit-yolo.git
cd gree-fruit-yolo
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```
## 3. 上传一个现有的文件夹（existing_folder/）
```
cd existing_folder
git init
git remote add origin http://10.2.11.226/iot-7/fruit/gree-fruit-yolo.git
git add .
git commit -m "Initial commit"
git push -u origin master
```
## 3+  Push an existing Git repository
```
cd existing_repo
git remote rename origin old-origin
git remote add origin http://10.2.11.226/iot-7/fruit/gree-fruit-yolo.git
git push -u origin --all
git push -u origin --tags
```

## 4. 重置git中的用户信息和密码
遇到下面报错时，多半是由于git中预置的密码与gitlab密码不匹配导致。
```
remote: HTTP Basic: Access denied
fatal: Authentication failed for 'http://gitlab.***.com/***.git/'
```
通过git命令对密码进行重置
```
git config --system --unset credential.helper
```
这里一定要以管理员身份打开，不然会出现：
> error: could not lock config file C:/Program Files/Git/mingw64/etc/gitconfig: Permission denied

再执行远程操作，会提示输入远程端的用户名和密码重新输入远程端的用户名和密码

本以为按上述操作就完美结束了，但后面发现每次操作远程仓库都需要重新输入用户名和密码，原因是`git config --system --unset credential.helper`这个命令清空`gitconfig`里的自动保存用户名和密码配置，找到本地的`gitconfig`文件，写入：
```
##如果不想保存，则删除即可
[credential]
    helper = store
```
这样你只需要再输入一次用户名和密码，系统就会自动保存你的用户名和密码。

## 5. 如何解决failed to push some refs to git
大概原因就是，本地和远程的文件应该合并后才能上传本地的新文件
```
git pull --rebase origin master 
git push -u origin master
```
## 6. .gitignore文件不起作用的解决办法
原因是git在之前版本是已经记录的所需要忽略的文件，可以按照以下步骤调整
1. `git rm -r --cached .` 删除本地的git缓存
2. 修改.gitignore文件，列入要隐藏的文件名或路径
3. `git add .`
4. `git commit -m '上传调整记录'`

## 7. git拉取远程分支
当在远程仓库新建一个分支时，由于本地的仓库还未同步，需要先同步再拉去，具体操作如下
1. `git pull`拉取远程分支到本地
2. `git checkout 分支名`切换本地仓库到新建的分支