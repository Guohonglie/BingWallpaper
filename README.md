### 如何使用

1.  在您的 GitHub `BingWallpaper` 仓库主页，点击绿色的 **"Add a README"** 按钮。
2.  GitHub 会为您创建一个名为 `README.md` 的文件，并打开一个编辑框。
3.  将下面 **"---" 分割线之间的所有内容** 完整地复制并粘贴到编辑框中。
4.  （可选）您可以在“# iWatch 每日必应壁纸自动化”下面写几句您自己的话。
5.  点击页面底部的绿色按钮 **"Commit new file"** 保存即可。

---

# iWatch 每日必应壁纸自动化

这是一个基于 GitHub Actions 的全自动化项目，旨在为我的 Apple Watch 每日自动更换一张来自 Bing 的高清壁纸。

## ✨ 项目特点

- **全自动运行**：无需任何人工干预，每日自动抓取、更新壁纸。
- **云端执行**：所有任务均由 GitHub Actions 在云端服务器完成，不占用本地资源。
- **稳定可靠**：通过固定的图片链接，确保 iWatch 快捷指令能稳定获取图片。
- **零成本**：完全利用 GitHub 的免费服务。

## 🚀 工作流程

1.  **定时触发**：GitHub Actions 工作流 (`.github/workflows/main.yml`) 每日定时（北京时间早上6点）启动。
2.  **执行脚本**：云端服务器运行 Python 脚本 (`download_wallpaper.py`)，访问 `bingwalls.com` 并解析出当天最新的高清壁纸下载链接。
3.  **下载与覆盖**：脚本将下载的壁纸统一命名为 `daily-wallpaper.jpg`。
4.  **自动提交**：工作流将新下载的 `daily-wallpaper.jpg` 自动提交并推送到本仓库，实现对旧壁纸的覆盖更新。
5.  **提供链接**：项目通过 `raw.githubusercontent.com` 提供一个永久固定的图片访问链接。

## 🔗 固定壁纸链接

我的 iWatch 快捷指令将从以下链接获取每日更新的壁纸：

```
https://raw.githubusercontent.com/Guohonglie/BingWallpaper/master/daily-wallpaper.jpg
```

## 🛠️ 技术栈

- **自动化**: GitHub Actions
- **脚本语言**: Python
- **核心库**: `requests`, `beautifulsoup4`

---

这个 README 文件不仅解释了项目是做什么的，还清晰地列出了它的工作流程和核心技术，非常专业！
