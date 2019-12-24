# liunx后台运行方法
## 创建新窗口
`screen`
## 创建新窗口，“-S name01” 是给窗口命名，让你容易识别
`screen -S name01`

## 窗口后台运行，让screen创建的窗口后台运行，我们返回主窗口做其它操作
`同时按下 Ctrl键 + A键 + D键`

## 查看srceen列表
`screen -ls  # 或者 screen -list `

## 切换到之前分离的窗口，输入窗口名称或者ID号都可以
`screen -r name01`

## 关闭某个处于attached状态的窗口
```
screen -X -S 你想关闭的窗口的名称 quit
screen -X -S name01 quit
```