# pip install zhipuai 请先在终端进行安装

from zhipuai import ZhipuAI
import os

ZHIPU_TOKEN = os.getenv("ZHIPU_TOKEN")

client = ZhipuAI(api_key=ZHIPU_TOKEN)  # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请仔细描述这个图片"},
                {"type": "image_url", "image_url": {"url": "https://xxx.jpg"}},
            ],
        }
    ],
    top_p=0.7,
    temperature=0.95,
    max_tokens=1024,
    stream=True,
)
for trunk in response:
    print(trunk)
