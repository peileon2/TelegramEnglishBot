## Google Cloud and Docker 部署心得

### 书写dockerfile

#### 配置port和main入口

```python
# Cloud Run 需要监听 0.0.0.0:$PORT
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
```

#### 配置dockerfile中的port配置

```dockerfile
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
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
```

1. 安装Python
   1. slim是简化版python
2. 设置入口
3. 安装poetry
4. 复制所有文件
5. 安装依赖环境
6. 端口确认
7. 启动代码

### 制作Docker镜像

```cmd
docker build -t my-fastapi-app .
docker run -p 8080:8080 my-fastapi-app
```

docker镜像由几部分组成

1. 镜像名字

2. Tag

   1. ```cmd
      docker build -t my-fastapi-app:v1.0 .
      # 这里:v1.0 就是为了打Tag
      ```

   2. 不给镜像显式指定 tag，默认就是 `latest`。

3. 端口

   1. 端口对照：-p <宿主机端口>:<容器端口>

4. 容器

   1. 镜像可以生成容器，容器会通过调用 入口运行

### 上传镜像

#### 上传到dockerhub

为了上传镜像到 Docker Hub，你需要给本地镜像打一个标签（Tag），标签的格式为：`<Docker Hub 用户名>/<镜像名称>:<标签>`。

假设你有一个本地镜像 `my-fastapi-app`，并且希望将其上传到 Docker Hub。你可以使用以下命令给它打标签：

```cmd
docker tag my-fastapi-app peio/myrepo:latest
给本地的my-fastapi-app 打上标签 peio/myrepo:latest
```

此处的peio/myrepo:latest, 前面时用户名，后面是仓库名

```cmd
docker push peio/myrepo:latest
```

注意上述代码，是根据tag来push。Tag类似于地址值

#### 上传google cloud

##### 本地和项目相匹配

```cmd
gcloud config set project your-gcp-project-id
```

```cmd
gcloud projects list
查看所有projects
```

##### 打Tag

docker tag [本地镜像名称] [GCP Artifact Registry 镜像路径]

```cmd
docker tag leonpei/firstdocker asia-east1-docker.pkg.dev/my-gcp-project/my-repo/firstdocker:latest
```

```
asia-east1-docker.pkg.dev/my-gcp-project/my-repo
# 命名规则
```

```cmd
docker push us-west2-docker.pkg.dev/cloudtry-448805/telebotdocker/firstdocker:latest
# push到仓库
```

##### 设置预算

### 查看镜像和项目

#### 查看gcloud

```cmd
gcloud projects list
```

#### 查看 docker

```cmd
docker images
```

