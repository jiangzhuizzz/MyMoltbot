# Mac Mini 新机设置指南

> 针对：首次使用Mac系统的Windows用户
> 
> 目标：快速配置开发和工作环境

---

## 📦 第一天：系统初始化

### 1.1 开机设置

首次开机后会进入设置向导：

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 选择语言 | 选"简体中文" |
| 2 | 地区 | 选"中国" |
| 3 | 键盘 | 添加"中文拼音" |
| 4 | WiFi | 连接网络 |
| 5 | Apple ID | 登录（没有就注册） |
| 6 | 条款 | 同意 |
| 7 | 创建账户 | 设置用户名和密码 |
| 8 | Siri | 建议开启 |
| 9 | 分析 | 建议开启 |

### 1.2 必做设置

#### 系统偏好设置（齿轮图标）

**触控板**（非常重要）：
```
系统偏好设置 → 触控板
→ 勾选"轻点来点按"
→ 勾选"辅助点按"（右键）
→ 勾选"放大缩小"
→ 勾选"智能缩放"
```

**鼠标**（如果你用鼠标）：
```
系统偏好设置 → 鼠标
→ 勾选"辅助点按"（右键）
→ 调整滚动方向（习惯）
```

**Dock栏**：
```
系统偏好设置 → 程序坞与菜单栏
→ 自动隐藏：开启
→ 窗口放大：开启
```

### 1.3 快捷键切换（重要！）

Mac和Windows快捷键差异：

| 功能 | Windows | Mac |
|------|---------|-----|
| 复制 | Ctrl+C | ⌘+C |
| 粘贴 | Ctrl+V | ⌘+V |
| 撤销 | Ctrl+Z | ⌘+Z |
| 剪切 | Ctrl+X | ⌘+X |
| 保存 | Ctrl+S | ⌘+S |
| 全选 | Ctrl+A | ⌘+A |
| 查找 | Ctrl+F | ⌘+F |
| 新建 | Ctrl+N | ⌘+N |
| 关闭窗口 | Alt+F4 | ⌘+Q |
| 切换窗口 | Alt+Tab | ⌘+Tab |
| 返回 | Backspace | ⌘+Delete |
| 强制退出 | Ctrl+Shift+Esc | ⌘+Option+Esc |
| 截图 | Win+Shift+S | ⌘+Shift+4 |

**符号说明**：
- ⌘ = Command键（通常在空格键旁边，有四叶草图标）
- ⌥ = Option/Alt键
- ⌃ = Control键
- ⇧ = Shift键

---

## 📦 第二天：安装必备软件

### 2.1 系统工具

#### Homebrew（必装！包管理器）
```bash
# 打开"终端"（Launchpad → 其他 → 终端）
# 粘贴以下命令，按回车

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装过程中会要求输入密码（开机密码），注意输入时不显示。

#### Git（版本控制）
```bash
# Homebrew安装
brew install git

# 验证
git --version
```

#### Xcode命令行工具
```bash
# 提示时安装，或手动执行
xcode-select --install
```

### 2.2 开发工具

#### Visual Studio Code（代码编辑器）
```bash
# Homebrew安装
brew install --cask visual-studio-code
```

或官网下载：https://code.visualstudio.com/

#### Python
Mac自带Python，建议安装最新版：
```bash
# 安装pyenv（管理多个Python版本）
brew install pyenv

# 安装Python 3.11
pyenv install 3.11.0

# 设置全局版本
pyenv global 3.11.0

# 验证
python --version
```

#### Node.js（用于Clawdbot等工具）
```bash
# 安装nvm（管理Node版本）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重启终端后
nvm install --lts

# 验证
node -v
```

### 2.3 常用软件

| 软件 | 安装命令 | 用途 |
|------|----------|------|
| Google Chrome | `brew install --cask google-chrome` | 浏览器 |
| Obsidian | `brew install --cask obsidian` | 知识库 |
| Iterm2 | `brew install --cask iterm2` | 高级终端 |
| Rectangle | `brew install --cask rectangle` | 窗口管理 |
| eZip | App Store下载 | 解压缩 |
|腾讯柠檬 | App Store下载 | 系统清理 |

---

## 📦 第三天：配置开发环境

### 3.1 配置Git
```bash
# 设置用户名
git config --global user.name "你的名字"

# 设置邮箱（与GitHub邮箱一致）
git config --global user.email "your@email.com"

# 设置默认编辑器
git config --global core.editor "code --wait"

# 查看配置
git config --list
```

### 3.2 SSH密钥（连接GitHub）
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "your@email.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub
```

复制公钥，添加到GitHub：
- GitHub → Settings → SSH and GPG keys → New SSH key

### 3.3 克隆项目
```bash
# 创建工作目录
mkdir -p ~/workspaces

# 克隆项目
cd ~/workspaces
git clone git@github.com:jiangzhuizzz/MyMoltbot.git
```

### 3.4 安装项目依赖
```bash
cd ~/workspaces/MyMoltbot

# 安装Node依赖
npm install

# 安装Python依赖（如果有requirements.txt）
pip install -r requirements.txt
```

---

## 📦 第四天：配置常用工具

### 4.1 安装zsh和oh-my-zsh（更好的终端）

```bash
# 安装zsh
brew install zsh

# 安装oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 重启终端生效
```

### 4.2 配置别名（.zshrc）
```bash
# 编辑配置
code ~/.zshrc

# 添加常用别名
alias gs="git status"
alias gc="git commit -m"
alias gp="git push"
alias gl="git pull"
alias cdw="cd ~/workspaces"
alias cdm="cd ~/workspaces/MyMoltbot"
alias python="python3"
alias pip="pip3"

# 保存后生效
source ~/.zshrc
```

### 4.3 安装Docker（可选）
```bash
# 安装Docker Desktop
brew install --cask docker

# 启动Docker Desktop
# 在Launchpad中点击Docker图标
```

---

## 📦 第五天：Obsidian配置

### 5.1 打开项目
```bash
# 打开ObsidianVault
cd ~/workspaces/MyMoltbot/obsidian-templates
```

### 5.2 启用必要插件

在Obsidian中：
1. **设置** → **第三方插件** → **关闭安全模式**
2. 安装并启用：
   - **Templater** - 模板
   - **Dataview** - 数据查询
   - **Obsidian Git** - Git备份

### 5.3 配置Templater
1. 新建`templates`文件夹
2. 设置 → Templater → 选择templates文件夹

---

## 📦 第六天：效率配置

### 6.1 常用快捷键速查

#### 系统快捷键
| 功能 | 快捷键 |
|------|--------|
| 截屏 | ⌘+Shift+4 |
| 截屏到剪贴板 | ⌘+Ctrl+Shift+4 |
| 显示桌面 | F11 |
| 快速搜索 | ⌘+空格 |
| 打开启动台 | Launchpad中四指张开 |
| 显示所有窗口 | 四指捏合 |

#### VS Code快捷键
| 功能 | 快捷键 |
|------|--------|
| 命令面板 | ⌘+Shift+P |
| 侧边栏 | ⌘+B |
| 终端 | ⌘+` |
| 多光标 | ⌘+Click |
| 格式化代码 | Shift+Option+F |
| 行注释 | ⌘+/ |

### 6.2 设置Rectangle（窗口管理）
- 快捷键：⌘+Option+数字
- 快速把窗口移到左边/右边/角落

### 6.3 设置Spotlight搜索
- ⌘+空格 打开
- 可以搜索文件、应用、计算器

---

## 📦 第七天：备份与恢复

### 7.1 Time Machine备份
1. 准备一个移动硬盘（至少256GB）
2. 系统偏好设置 → Time Machine
3. 选择备份磁盘
4. 开启自动备份

### 7.2 配置iCloud同步
- 打开系统偏好设置 → Apple ID
- 开启iCloud Drive
- 重要文件自动同步

### 7.3 重要文件位置

| 文件 | 位置 |
|------|------|
| 桌面 | ~/Desktop |
| 文档 | ~/Documents |
| 下载 | ~/Downloads |
| 工作目录 | ~/workspaces |
| 配置文件 | ~/.zshrc, ~/.gitconfig |

---

## 💡 常见问题

### Q1: 鼠标滚轮方向反了？
```
系统偏好设置 → 触控板 → 滚动和缩放
→ 取消勾选"自然方向"
```

### Q2: 找不到Command键？
Mac键盘布局：
```
┌─────────┬─────────┬─────────┬─────────┐
│  fn     │  ⌥     │  ⌘     │  ⌃     │
│ 功能键  │  Alt   │  Command│ Control │
└─────────┴─────────┴─────────┴─────────┘
```

### Q3: 怎么安装Windows软件？
Mac不能直接安装Windows软件，但可以用：
- **CrossOver**（付费）
- **虚拟机Parallels/VMware**（付费）
- **双系统**（不建议）

### Q4: 怎么卸载软件？
1. 在Launchpad中长按图标
2. 点击"×"删除
3. 或打开"访达" → "应用程序" → 拖到废纸篓

### Q5: 终端打不开？
1. 打开"系统偏好设置" → "安全性与隐私"
2. 点击"隐私"标签
3. 选中"完全磁盘访问权限"
4. 勾选"终端"

---

## 📋 快速安装命令汇总

```bash
# 1. Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 开发工具
brew install git
brew install --cask visual-studio-code
brew install --cask obsidian
brew install --cask iterm2
brew install --cask rectangle
brew install --cask google-chrome

# 3. Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 4. Python
brew install pyenv

# 5. Git配置
git config --global user.name "你的名字"
git config --global user.email "your@email.com"
```

---

## 🎯 优先级清单

### 必做（第一天）
- [ ] 完成系统初始化
- [ ] 配置触控板
- [ ] 熟悉Command键位置

### 必装（第二天）
- [ ] Homebrew
- [ ] Git
- [ ] VS Code
- [ ] Obsidian

### 必配（第三天）
- [ ] Git配置
- [ ] SSH密钥
- [ ] 克隆项目

### 推荐（第四-五天）
- [ ] oh-my-zsh
- [ ] 启用Obsidian插件
- [ ] 设置别名

---

## 🔧 技术支持

### 遇到问题怎么办？

1. **百度/Google搜索错误信息**
2. **查看官方文档**
   - Mac: https://support.apple.com/zh-cn
   - Homebrew: https://brew.sh
   - VS Code: https://code.visualstudio.com/docs
3. **问AI助手**（比如我）

---

*制定时间：2026-02-01*
*预计设置时间：7天*
