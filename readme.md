# Python 开发环境配置笔记

本文档整理了 Python 开发中常用的环境配置方法,包括虚拟环境管理、依赖管理、镜像加速等。

---

## 目录

- [Windows 环境配置](#windows-环境配置)
  - [1. 安装 virtualenv 并创建虚拟环境](#1-安装-virtualenv-并创建虚拟环境)
  - [2. 导出依赖(requirements.txt)](#2-导出依赖requirementstxt)
  - [3. 在新环境中恢复依赖](#3-在新环境中恢复依赖)
  - [4. py 启动器(多版本管理)](#4-py-启动器多版本管理)
  - [5. 加速 pip 下载](#5-加速-pip-下载)
- [Debian 环境配置](#debian-环境配置)
  - [pyenv 版本管理](#pyenv-版本管理)
  - [内嵌式虚拟环境(venv)](#内嵌式虚拟环境venv)
  - [pip 加速](#pip-加速)
- [Docker](#docker)

---

## Windows 环境配置

### 1. 安装 virtualenv 并创建虚拟环境

安装虚拟环境工具:

```bash
pip install virtualenv
```

创建虚拟环境:

```bash
virtualenv .venv
```

激活虚拟环境(PowerShell):

```powershell
.\.venv\Scripts\activate.ps1
```

### 2. 导出依赖(requirements.txt)

把代码分享给别人或上传到 GitHub 时,在激活的虚拟环境下运行:

```powershell
# 不附带 Python 版本
pip freeze > requirements.txt

# 附带 Python 版本
echo "# Python version: $(python3 -V)" > requirements.txt && pip freeze >> requirements.txt
```

这会生成一个 `requirements.txt` 文件,记录了项目用到的所有包和对应版本。把这个文件提交到 Git。

### 3. 在新环境中恢复依赖

从 Git 下载代码后,只需要两步即可恢复环境:

1. 创建并激活新的虚拟环境:

   ```bash
   virtualenv .venv
   ```

2. 一键安装所有依赖:

   ```bash
   pip install -r requirements.txt
   ```

### 4. py 启动器(多版本管理)

在 Windows 上装了多个 Python 版本时,可以使用 `py` 启动器指定版本:

```powershell
py -0                       # 列出电脑上所有已安装的 Python 版本
py -3.9                     # 用 3.9 版本运行交互式解释器
py -3.11 script.py          # 用 3.11 运行脚本
py -3.11 -m venv venv312    # 用 3.11 创建虚拟环境
py -3.11 -m venv .venv
```

### 5. 加速 pip 下载

主要思路是切换到国内镜像源,以及一些辅助优化手段。

#### 方法一:临时使用镜像源(单次安装)

```powershell
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 常用国内镜像

| 镜像源 | 地址 |
| --- | --- |
| 清华大学 | <https://pypi.tuna.tsinghua.edu.cn/simple> |
| 阿里云 | <https://mirrors.aliyun.com/pypi/simple/> |
| 中国科技大学 | <https://pypi.mirrors.ustc.edu.cn/simple/> |
| 华为云 | <https://repo.huaweicloud.com/repository/pypi/simple/> |
| 腾讯云 | <https://mirrors.cloud.tencent.com/pypi/simple/> |

#### 方法二:永久配置(推荐,一次设置全局生效)

Windows 配置文件路径为 `%APPDATA%\pip\pip.ini`(没有就新建):

```powershell
# 先创建目录(如果不存在)
mkdir %APPDATA%\pip
notepad %APPDATA%\pip\pip.ini
```

写入以下内容:

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

也可以用命令直接写配置,无需手动编辑:

```powershell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

设置好之后,以后 `pip install xxx` 都会自动走这个源,不用每次加 `-i` 参数。

#### 方法三:多版本 Python 验证

因为装了多版本 Python,可以每个版本都检查一下是否生效(镜像配置是全局的,通常一次设置对所有版本都生效):

```powershell
py -3.9 -m pip config list
py -3.11 -m pip config list
py -3.12 -m pip config list
```

#### 方法四:升级 pip 本身 + 使用缓存

```powershell
py -3.12 -m pip install --upgrade pip
```

pip 默认会缓存已下载的包(在 `%LOCALAPPDATA%\pip\Cache`),重复安装同一版本包时更快,一般不需要额外配置。

#### 额外提示

- 如果公司/学校有内网镜像,速度通常比公网镜像更快,可以优先使用。
- 如果某个源临时抽风很慢,换另一个镜像源试试即可。
- 用 [uv](https://github.com/astral-sh/uv)(新一代包管理工具)替代 pip 也是个选择,下载和解析速度明显更快,而且能自动利用镜像配置。

---

## Debian 环境配置

### pyenv 版本管理

`pyenv` 是一个 Python 版本管理工具,常用命令如下。

#### 安装版本

```bash
pyenv install 3.11.0      # 安装指定版本
pyenv versions            # 查看所有已安装的 Python 版本和虚拟环境
pyenv virtualenvs         # 仅查看所有的虚拟环境
```

#### 切换版本

```bash
pyenv global 3.11.0        # 设置全局默认版本
pyenv local 3.11.0         # 在当前目录创建 .python-version 文件
pyenv shell 3.11.0         # 设置当前 shell 会话版本
```

#### 创建虚拟环境

```bash
pyenv virtualenv 3.11.0 myenv       # 基于某版本创建虚拟环境
pyenv activate myenv                # 激活虚拟环境
pyenv deactivate                    # 退出虚拟环境
pyenv uninstall myenv               # 删除虚拟环境
```

#### 其他常用命令

```bash
pyenv uninstall 3.11.0      # 卸载版本
pyenv which python          # 查看当前 Python 路径
pyenv rehash                # 更新 shims(安装新版本后需要)
```

### 内嵌式虚拟环境(venv)

Debian 自带 `venv` 模块,无需额外安装:

```bash
cd /path/to/project         # 1. 进入项目目录

python -m venv .venv        # 2. 在当前目录下创建名为 .venv 的虚拟环境文件夹(Linux 下加 . 表示隐藏文件夹)

source .venv/bin/activate   # 3. 激活环境

deactivate                  # 4. 退出虚拟环境
```

### pip 加速

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

---

## Docker

启动 MySQL 容器示例:

```bash
docker run -d \
  --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=654321 \
  -e MYSQL_DATABASE=mydb \
  -e MYSQL_USER=myuser \
  -e MYSQL_PASSWORD=aabbcc \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  mysql:8.0.39
```

或使用 docker compose:

```bash
docker compose -f ./mysql-setup.yml up -d
```