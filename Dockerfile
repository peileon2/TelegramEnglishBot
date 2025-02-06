# 使用官方 Python 3.11 slim 版本作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 Poetry（官方推荐方式）
RUN pip install --no-cache-dir poetry

# 复制整个项目文件夹
COPY . /app/

# 使用 Poetry 安装依赖
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi
ENV PORT=8080
# 暴露端口
EXPOSE 8080

# 使用 bash 来启动 FastAPI 应用，确保环境变量可以被解析
CMD ["sh", "-c", "poetry run uvicorn app:app --host 0.0.0.0 --port $PORT"]
