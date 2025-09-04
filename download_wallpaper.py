# -*- coding: utf-8 -*-
"""
Bing Wallpaper Downloader for GitHub Actions (Final Robust Version)
- This script is a fusion of the original powerful script and best practices for cloud automation.
- It robustly finds the download link and saves the image with a fixed filename.
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def find_download_link(soup, page_url):
    """
    (来自您的原始代码) 查找下载链接的强大函数。
    它结合了两种策略，以确保最大可能地找到链接。
    """
    # 方法1: 查找文本中包含 "4k", "download" 等关键词的下载按钮
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text().strip().lower()
        if any(keyword in text for keyword in ['4k', 'download', 'uhd', '下载']):
            if 'storage/bing-wallpapers/' in href:
                full_url = urljoin(page_url, href)
                print(f"  ✅ [策略1] 通过下载按钮找到链接: {full_url}")
                return full_url

    # 方法2: 如果找不到按钮，就直接在页面的图片(img)标签里寻找
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'bing-wallpapers' in src:
            full_url = urljoin(page_url, src)
            print(f"  ✅ [策略2] 通过图片标签找到链接: {full_url}")
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
    # BingWalls的壁纸通常是前一天的，所以我们获取昨天的日期
    # 使用 UTC 时间，因为 GitHub Actions 的服务器通常使用 UTC
    yesterday_utc = datetime.utcnow() - timedelta(days=1)
    date_str = yesterday_utc.strftime("%Y-%m-%d") # 使用 YYYY-MM-DD 格式，这在您的原始代码中是有效的

    page_url = f"https://bingwalls.com/china/{date_str}"
    
    print(f"🚀 开始处理日期 (UTC): {date_str}")
    print(f"📄 正在访问页面: {page_url}")

    try:
        response = requests.get(page_url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 使用您原始代码中的强大查找函数
        download_url = find_download_link(soup, page_url)

        if not download_url:
            print("  ❌ 未能在页面上找到有效的下载链接。")
            sys.exit(1)

        if not download_image(download_url, OUTPUT_FILENAME):
            sys.exit(1)

        print("🎉 任务成功完成！")

    except requests.exceptions.RequestException as e:
        # 打印更详细的错误信息，包括状态码
        error_message = f"  ❌ 访问页面时发生错误: {e}"
        if e.response is not None:
            error_message += f" (Status Code: {e.response.status_code})"
        print(error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()
