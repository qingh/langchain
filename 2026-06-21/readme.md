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



py -0                       # 列出电脑上所有已安装的 Python 版本
py -3.9                     # 用 3.9 版本运行交互式解释器
py -3.11 script.py          # 用 3.11 运行脚本
py -3.11 -m venv venv312    # 用 3.12 创建虚拟环境
py -3.11 -m venv .venv



加速 pip 下载

主要思路是切换到国内镜像源,以及一些辅助优化手段。

方法一：临时使用镜像源(单次安装)
powershell
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple

常用国内镜像：

镜像源	地址
清华大学	https://pypi.tuna.tsinghua.edu.cn/simple
阿里云	https://mirrors.aliyun.com/pypi/simple/
中国科技大学	https://pypi.mirrors.ustc.edu.cn/simple/
华为云	https://repo.huaweicloud.com/repository/pypi/simple/
腾讯云	https://mirrors.cloud.tencent.com/pypi/simple/
方法二：永久配置(推荐,一次设置全局生效)

Windows 下配置文件路径是 %APPDATA%\pip\pip.ini(没有就新建)：

powershell
# 先创建目录(如果不存在)
mkdir %APPDATA%\pip
notepad %APPDATA%\pip\pip.ini

写入以下内容：

ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn

也可以用命令直接写配置,不用手动编辑文件：

powershell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

设置好之后,以后 pip install xxx 都会自动走这个源,不用每次加 -i 参数。

方法三：针对多个 Python 版本分别验证

因为你装了多版本 Python,记得每个版本的 pip 都检查一下是否生效(镜像配置是全局的,通常一次设置对所有版本都生效,但可以验证一下)：

powershell
py -3.9 -m pip config list
py -3.11 -m pip config list
py -3.12 -m pip config list
方法四：升级 pip 本身 + 使用缓存
powershell
py -3.12 -m pip install --upgrade pip

pip 默认会缓存已下载的包(在 %LOCALAPPDATA%\pip\Cache),重复安装同一版本包时会更快,一般不需要额外配置。

额外提示
如果公司/学校有内网镜像,速度通常比公网镜像更快,可以优先使用
如果某个源临时抽风很慢,换另一个镜像源试试即可,几个源之间切换很简单
用 uv(新一代包管理工具)替代 pip 也是个选择,下载和解析速度明显更快,而且能自动利用镜像配置

需要我帮你写一个一键切换镜像源的脚本吗？