# -*- coding: utf-8 -*-

import os
import urllib.parse

from PIL import Image
from pyppeteer import launch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
import imageio.v2 as imageio
from flask import Response


# 指定url区域截屏保存成pdf
async def url_save_pdf(url, pdf_path, resolution, clip):
    start_parm = {
        # 下列三个参数用于解决 Flask 运行 Pyppeteer 报错 "signal only works in main thread"
        "handleSIGINT": False,
        "handleSIGTERM": False,
        "handleSIGHUP": False,
        "headless": True,    # 关闭无头浏览器
        "args": [
            '--no-sandbox',  # 关闭沙盒模式
        ],
    }
    browser = await launch(**start_parm)
    page = await browser.newPage()
    # 加载指定的网页url
    await page.goto(url)
    # 设置网页显示尺寸
    await page.setViewport(resolution)
    # 设置截屏区域
    if 'x' not in clip or 'y' not in clip:
        await page.pdf({'path': pdf_path, 'width': clip['width'], 'height': clip['height']})
        await browser.close()
    else:
        img_data = await page.screenshot({'clip': clip})
        img_data_array = imageio.imread(img_data, format="png")
        im = Image.fromarray(img_data_array)
        page_width, page_height = im.size
        c = Canvas(pdf_path, pagesize=(page_width, page_height))
        c.drawImage(ImageReader(im), 0, 0)
        c.save()


# 检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# 将文件转成文件流提供下载
def download_file(file_path):

    # 文件路径、文件名、后缀分割
    file_dir, file_full_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_full_name)

    # 文件名如果包含中文则进行编码
    if is_contains_chinese(file_name):
        file_name = urllib.parse.quote(file_name)
    new_file_name = file_name + file_ext

    # 流式读取下载
    def send_file():
        with open(file_path, 'rb') as targetfile:
            while 1:
                data = targetfile.read(20 * 1024 * 1024)   # 每次读取20M
                if not data:
                    break
                yield data
    response = Response(send_file(), content_type='application/octet-stream')
    response.headers["Content-disposition"] = 'attachment; filename=%s' % new_file_name
    return response
