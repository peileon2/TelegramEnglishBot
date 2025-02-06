from zhipuai import ZhipuAI
import os

ZHIPU_TOKEN = os.getenv("ZHIPU_TOKEN")

client = ZhipuAI(api_key=ZHIPU_TOKEN)  # 填写您自己的APIKey


class ZhipuWord:
    def __init__(self, api_key: str, model: str = "GLM-4-Flash"):
        self.client = ZhipuAI(api_key=api_key)  # 初始化API客户端
        self.model = model  # 设置默认的模型名称

    def generate_slogan(
        self,
        product_info: str,
        initial_message: str = "作为一名营销专家，请为我的产品创作一个吸引人的口号",
    ):
        # 构造聊天消息
        messages = [
            {"role": "user", "content": initial_message},
            {
                "role": "assistant",
                "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息",
            },
            {"role": "user", "content": product_info},
            {
                "role": "assistant",
                "content": "点燃未来，智谱AI绘制无限，让创新触手可及！",
            },
            {"role": "user", "content": "创作一个更精准且吸引人的口号"},
        ]

        # 获取AI回复
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )

        # 返回生成的口号
        print(response.choices[0].message.content)
        return response.choices[0].message.content  # 使用示例


zhipu = ZhipuWord

product_info = "智谱AI开放平台"
slogan = zhipu.generate_slogan(product_info)

print(slogan)
