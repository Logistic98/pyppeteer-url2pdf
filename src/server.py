# -*- coding: utf-8 -*-

import json
import time
from uuid import uuid1
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_docs import ApiDoc
import os
import asyncio

from log import logger
from responseCode import ResponseCode, ResponseMessage
from utils import url_save_pdf, download_file

# 创建一个服务
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Flask-Doc接口文档
ApiDoc(
    app,
    title="Flask-Doc接口文档",
    version="1.0.0",
    description="Flask API Doc",
)

api = Blueprint("api", __name__)
app.config["API_DOC_MEMBER"] = ["api"]


@api.route("/pyppeteer/urlSavePdf", methods=["POST"])
def urlSavePdf():
    """将任意公开访问的url转化为pdf提供下载
    @@@
    ### args
    |  args | required | request type | type |  remarks |
    |-------|----------|--------------|------|----------|
    | url |  true    |    body      | str  | 目标网址url   |
    | pdf_name |  false    |    body      | str  | pdf文件名称   |
    | resolution |  false    |    body      | object  | 网页显示尺寸   |
    | clip |  false    |    body      | object  | 位置与图片尺寸信息   |

    参数说明：
    ```json
     url：可公开访问的目标网址（必填，不能是那种需要登录权限的）
     pdf_name：下载的pdf文件（非必填，默认值是uuid命名的pdf文件）
     clip: 位置与图片尺寸信息（非必填，默认值{"width": 1920, "height": 1680}）
         x: 网页截图的起始x坐标
         y: 网页截图的起始y坐标
         width: 图片宽度
         height: 图片高度
     注释：只传width、height的时候为整页导出，传x，y，width、height的时候为区域导出
     resolution: 设置网页显示尺寸 （非必填，默认值{"width": 1920, "height": 1680}）
         width: 网页显示宽度
         height: 网页显示高度
    ```

    ### request
    ```json
    {
        "url":"https://www.google.com",
        "pdf_name":"test.pdf",
        "resolution": {"width": 1920, "height": 1680},
        "clip": {"x": 0, "y": 0, "width": 1920, "height": 1680}
    }
    ```

    ### return
    ```json
    以文件流的形式提供pdf文件下载
    ```
    @@@
    """
    return jsonify({"code": 200, "msg": "xxx", "data": "xxx"})


app.register_blueprint(api, url_prefix="/docs/api")
logger.info('接口文档地址：http://127.0.0.1:5006/docs/api/')


"""
# 将任意公开访问的url转化为pdf提供下载
"""
@app.route(rule='/api/pyppeteer/urlSavePdf', methods=['POST'])
def urlToPdf():
    # 获取JSON格式的请求体，并解析
    request_data = request.get_data(as_text=True)
    request_body = json.loads(request_data)

    # 参数校验模块
    url = request_body.get("url")
    if not url:
        fail_response = dict(code=ResponseCode.RARAM_FAIL, msg=ResponseMessage.RARAM_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)
    pdf_name = request_body.get("pdf_name")
    if not pdf_name:
        pdf_name = '{}.pdf'.format(uuid1())
    '''
     resolution: 设置网页显示尺寸
         width: 网页显示宽度
         height: 网页显示高度
     '''
    resolution = request_body.get("resolution")
    if not resolution:
        resolution = {"width": 1920, "height": 1680}
    '''
     clip: 位置与图片尺寸信息
         x: 网页截图的起始x坐标
         y: 网页截图的起始y坐标
         width: 图片宽度
         height: 图片高度
     '''
    clip = request_body.get("clip")
    if not clip:
        clip = {"width": 1920, "height": 1680}

    # 创建pdf的存储目录
    now_str = time.strftime("%Y%m%d", time.localtime())
    pdf_root_path = './tmp/'
    pdf_base_path = pdf_root_path + now_str
    if not os.path.exists(pdf_base_path):
        os.makedirs(pdf_base_path)
    pdf_path = pdf_base_path + '/' + pdf_name

    # 将url保存成pdf文件
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(url_save_pdf(url, pdf_path, resolution, clip))
        logger.info("成功将【{}】网址保存成pdf文件【{}】！".format(url, pdf_path))
    except Exception as e:
        logger.error(e)
        fail_response = dict(code=ResponseCode.BUSINESS_FAIL, msg=ResponseMessage.BUSINESS_FAIL, data=None)
        logger.error(fail_response)
        return jsonify(fail_response)

    # 将pdf文件转成文件流提供下载
    return download_file(pdf_path)


if __name__ == '__main__':
    # 解决中文乱码问题
    app.config['JSON_AS_ASCII'] = False
    # 启动服务，指定主机和端口
    app.run(host='0.0.0.0', port=5006, debug=False, threaded=True)
