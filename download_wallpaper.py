# -*- coding: utf-8 -*-
"""
Bing Wallpaper Downloader for GitHub Actions
- Downloads the latest wallpaper from BingWalls.
- Saves it with a fixed filename 'daily-wallpaper.jpg'.
- Designed to be run automatically in a cloud environment.
Author: Guohonglie (Refactored by AI for Actions)
Date: 2025-09-04
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin
import sys

# --- 配置区域 ---
# 输出的文件名（固定不变，用于在GitHub仓库中覆盖）
OUTPUT_FILENAME = "daily-wallpaper.jpg"
# 请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def find_download_link(html_content, page_url):
    """从HTML内容中解析出高清壁纸的下载链接"""
    soup = BeautifulSoup(html_content, 'html.parser')
    # 优先寻找包含 "4k", "download", "uhd" 等关键词的下载链接
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text().strip().lower()

        if any(keyword in text for keyword in ['4k', 'download', 'uhd', '下载']):
            if 'storage/bing-wallpapers/' in href:
                # 将相对路径拼接成完整的URL
                full_url = urljoin(page_url, href)
                print(f"  ✅ 成功找到下载链接: {full_url}")
                return full_url
    return None


def download_image(image_url, output_filename):
    """下载图片并保存到指定路径"""
    try:
        print(f"  📥 正在下载图片...")
        response = requests.get(image_url, headers=HEADERS, stream=True, timeout=30)
        # 检查请求是否成功
        response.raise_for_status()

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  👍 图片 '{output_filename}' 下载并保存成功!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 下载图片时发生错误: {e}")
        return False


def main():
    """主执行函数"""
    # BingWalls的壁纸通常是前一天的，所以我们获取昨天的日期
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y%m%d")

    page_url = f"https://bingwalls.com/china/{date_str}"
    print(f"🚀 开始处理日期: {date_str}")
    print(f"📄 正在访问页面: {page_url}")

    try:
        # 1. 获取每日壁纸所在的网页
        response = requests.get(page_url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        # 2. 从网页HTML中寻找下载链接
        download_url = find_download_link(response.content, page_url)

        if not download_url:
            print("  ❌ 未能在页面上找到有效的下载链接。")
            sys.exit(1)  # 退出并标记为失败，GitHub Actions会看到这个错误

        # 3. 下载图片
        if not download_image(download_url, OUTPUT_FILENAME):
            sys.exit(1)  # 下载失败，退出并标记为失败

        print("🎉 任务成功完成！")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ 访问页面时发生错误: {e}")
        sys.exit(1)  # 访问失败，退出并标记为失败


if __name__ == "__main__":
    main()