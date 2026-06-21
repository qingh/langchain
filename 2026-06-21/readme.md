安装虚拟环境工具
```
pip install virtualenv
```

用它来创建虚拟环境
```
virtualenv .venv
```
激活虚拟环境
```
.\.venv\Scripts\activate.ps1
```

2. 导出你的“菜单”
当你想把代码分享给别人，或者上传到 GitHub 时，在激活的虚拟环境下运行：

PowerShell
```
pip freeze > requirements.txt
```
这会生成一个非常小的文本文件 requirements.txt，里面记录了你这个项目用到了哪些包和对应的版本。把这个文件提交到 Git。

3. 别人（或未来的你）如何恢复环境？
当从 Git 上下载了代码后，只需要两步就能完美复活环境：

在新电脑上创建并激活全新的虚拟环境：virtualenv .venv

根据“菜单”一键安装所有依赖：
```
pip install -r requirements.txt
```