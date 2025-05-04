FROM python:3.8.8-slim

# python:3.8-slim 是基于 Debian GNU/Linux 10 (buster) 制作的
# 设置 Debian 清华源 https://mirrors.tuna.tsinghua.edu.cn/help/debian/（可选）
# RUN mv /etc/apt/sources.list /etc/apt/sources.list_bak && \
#    echo '# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释' >> /etc/apt/sources.list && \
#    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free' >> /etc/apt/sources.list && \
#    echo '# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free' >> /etc/apt/sources.list && \
#    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free' >> /etc/apt/sources.list && \
#    echo '# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free' >> /etc/apt/sources.list && \
#    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free' >> /etc/apt/sources.list && \
#    echo '# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free' >> /etc/apt/sources.list && \
#    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free' >> /etc/apt/sources.list && \
#    echo '# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free' >> /etc/apt/sources.list
# 下载无头 Chrome 依赖，参考：https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#chrome-headless-doesnt-launch-on-unix=
RUN apt-get update && apt-get -y install apt-transport-https ca-certificates libnss3 xvfb gconf-service libasound2  \
    libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0  \
    libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1  \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6  \
    ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget && rm -rf /var/lib/apt/lists/*

# 安装常用调试命令（可选）
RUN apt-get install iputils-ping -y           # 安装ping
RUN apt-get install -y wget                   # 安装wget
RUN apt-get install curl -y                   # 安装curl
RUN apt-get install vim -y                    # 安装vim
RUN apt-get install lsof                      # 安装lsof

# 安装msyh.ttc字体解决中文乱码问题
# 来源：https://github.com/owent-utils/font/raw/master/%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91/MSYH.TTC
RUN cp msyh.ttc /usr/share/fonts/

# 使用淘宝镜像加速下载 chromium（可选）
# ENV PYPPETEER_DOWNLOAD_HOST=https://npm.taobao.org/mirrors
# 设置 chromium 版本，发布日期为: 2021-02-26T08:47:06.448Z
ENV PYPPETEER_CHROMIUM_REVISION=856583

# 拷贝代码到容器内
RUN mkdir /code
ADD src /code/
WORKDIR /code

# 安装项目所需的 Python 依赖
RUN pip install -r requirements.txt

# 放行端口
EXPOSE 5006
# 启动项目
ENTRYPOINT ["nohup","python","server.py","&"]
