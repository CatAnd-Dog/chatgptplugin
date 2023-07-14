# 使用官方 Python 镜像作为基础镜像
FROM python:3.9.10

# 设置工作目录
WORKDIR /app


# 把当前目录（即你的 Flask 应用）下的所有文件拷贝到 Docker 镜像中的 /app 目录
COPY . .

# 安装 requirements.txt 中指定的 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口 15212 供应用使用
EXPOSE 15413

# 在容器启动时运行 Flask 应用
CMD ["python", "oneperfect.py"]