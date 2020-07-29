## git 合并分支操作

1. 首先，把项目克隆下来：
```
git clone http://10.2.11.226/201741/remote-job.git
```

2. 然后进入项目目录，建立一个自己的分支（名称自取），以便在自己的分支上工作：
```
cd remote-job
git checkout -b yzh
```
（git checkout 表示切换分支，-b 参数表示新建）

3. 开始修改项目里面的README文件（建议用Typora软件），并保存。

4. 修改完之后，进行暂存和版本提交这两个基本操作：
```
git add .
git commit -m "2月13日晚报"
```

5. 开始合并，合并前先尝试获取最新代码到本地 origin：
```
git fetch
```
（origin 代表着工程所关联的远程仓库）
（git fetch 会获取所有分支的最新代码到本地 orgin）

6. 然后对版本历史进行衍合：
```
git rebase origin/master
```

7. （若衍合的时候有冲突） 按照命令行提示继续修改文件，然后解决冲突：
```
git add .
git rebase --continue
```
（衍合后，你提交的版本就会基于最新版本。版本历史是一条直线，没有分叉）

8.  现在切换到主分支
```
git checkout master
```

9. 可以进行安全的合并了：
```
git merge yzh
```

10. 最后推送主分支:
```
git push origin master
```
（git push 默认推送当前分支，当前分支是master，因此亦可直接执行 git push）

12. 推送完之后切换回自己的分支
```
git checkout yzh
```

13. 第二天开发的时候，要记得合并最新主分支 master 到自己的分支 yzh：
```
 git pull origin master
```
（注意：git pull 执行的是拉取与合并两个操作） 
（git pull 默认拉取当前所在分支的远程分支与自己合并，当前分支已切换回 yzh，因此这里要指定远程分支为 master）

14. 接下来步骤同 3~12

（结束）
（建议实际项目开发的 git 操作步骤同上，但远程仓库要建立 dev 开发分支。
开发人员克隆代码后在 dev 分支上新建自己的分支，上传代码时只能推送 dev 分支。
master 用以保存稳定版本，仅项目管理员有权限合并）