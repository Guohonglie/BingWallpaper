# -*- coding: utf-8 -*-
"""
Bing Wallpaper Downloader for GitHub Actions (Robust Version)
- Downloads the latest wallpaper from BingWalls.
- Saves it with a fixed filename 'daily-wallpaper.jpg'.
- Uses a more robust method to find the download link.
Author: Guohonglie (Refactored by AI for Actions)
Date: 2025-09-04
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin
import sys

# --- 配置区域 ---
OUTPUT_FILENAME = "daily-wallpaper.jpg"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def find_download_link_robust(html_content, page_url):
    """
    更强大的下载链接查找函数。
    它直接寻找任何指向 'storage/bing-wallpapers/' 的链接，而不是依赖于链接的文本。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # 遍历页面上所有的超链接 (<a> 标签)
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        # 如果链接地址本身就包含了壁纸的存储路径，我们就认为这是正确的链接
        if 'storage/bing-wallpapers/' in href:
            full_url = urljoin(page_url, href)
            print(f"  ✅ (Robust) 成功找到下载链接: {full_url}")
            return full_url
    return None

def download_image(image_url, output_filename):
    """下载图片并保存到指定路径"""
    try:
        print(f"  📥 正在下载图片...")
        response = requests.get(image_url, headers=HEADERS, stream=True, timeout=30)
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
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Ym%d") # 注意: 这里的日期格式是 YYYYMMDD
    page_url = f"https://bingwalls.com/china/{date_str}"
    
    print(f"🚀 开始处理日期: {date_str}")
    print(f"📄 正在访问页面: {page_url}")

    try:
        response = requests.get(page_url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        # 使用我们新的、更强大的函数来寻找链接
        download_url = find_download_link_robust(response.content, page_url)

        if not download_url:
            print("  ❌ 未能在页面上找到有效的下载链接。")
            sys.exit(1)

        if not download_image(download_url, OUTPUT_FILENAME):
            sys.exit(1)

        print("🎉 任务成功完成！")

    except requests.exceptions.RequestException as e:
        print(f"  ❌ 访问页面时发生错误: {e} (URL: {page_url})")
        sys.exit(1)

if __name__ == "__main__":
    main()
