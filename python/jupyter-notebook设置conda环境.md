# jupyter notebook设置conda环境
通过jupyter notebook进行conda环境的切换

## 1、 选择要在Jupyter Notebook中激活的env，并激活
```
D:\github\learning-notes-hzg\python>conda activate hzg

(hzg) D:\github\learning-notes-hzg\python>conda env list
# conda environments:
#
base                     D:\ProgramData\Anaconda3
hzg                   *  D:\ProgramData\Anaconda3\envs\hzg
yolo-cpu                 D:\ProgramData\Anaconda3\envs\yolo-cpu
```

## 2、在要激活的环境中安装ipykernel
* `conda install ipykernel`

## 3、将选择的conda环境注入Jupyter Notebook
在该环境下输入以下指令

python -m ipykernel install --user --name *环境名* --display-name "Python [conda env:*环境名*]"