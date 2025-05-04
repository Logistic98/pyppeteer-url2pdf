## pyppeteer-url2pdf

### 1. 项目简介

使用Flask对puppeteer进行了封装，实现了将任意公开访问的url转化为pdf提供下载的功能

- puppeteer：Headless chrome/chromium 自动化库（是 [puppeteer](https://github.com/puppeteer/puppeteer) 的Python版非官方库），可用于网页截图导出pdf。

局限性：依赖于网络环境，目标网址过慢的话会出现未加载完即截屏的情况。

### 2. 项目部署

项目部署目录结构如下：

```
.
├── Dockerfile
├── README.md
├── build.sh
└── src
    ├── code.py
    ├── log.py
    ├── requirements.txt
    ├── msyh.ttc
    ├── response.py
    ├── server.py
    └── utils.py
```

安装docker环境，将部署包整个上传到服务器上，切换到部署包的根目录，执行如下脚本。

```
$ chmod u+x build.sh
$ ./build.sh
```

### 3. 接口文档

请求路径：/api/pyppeteer/urlSavePdf

请求方法：POST请求

请求参数：

```
 url：可公开访问的目标网址（必填，不能是那种需要登录权限的）
 pdf_name：下载的pdf文件名称（非必填，默认值是uuid命名的pdf文件）
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

请求示例：

```json
{
    "url":"https://www.google.com",
    "pdf_name":"test.pdf",
    "resolution": {"width": 1920, "height": 1680},
    "clip": {"x": 0, "y": 0, "width": 1920, "height": 1680}
}
```

接口返回：以文件流的形式提供pdf文件下载

### 4. 测试请求

```
$ curl -v -X POST http://127.0.0.1:5006/api/pyppeteer/urlSavePdf -H "Content-type: application/json" -d'{"url":"https://www.google.com","pdf_name":"test.pdf","resolution": {"width": 1920, "height": 1680},"clip": {"x": 0, "y": 0, "width": 1920, "height": 1680}}' >> test.pdf
```
