from openai import OpenAI
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY 环境变量未设置！")


class DeepSeekWord:
    def __init__(self, model: str = "deepseek-reasoner"):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
        )
        self.model = model  # 设置默认的模型名称

    def generate_text(self, content):
        messages = [
            {
                "role": "system",
                "content": """你是一个专业的英语写作和口语分析助手，能够帮助用户检查和改正英语句子。

        ### **任务要求**：
        1️⃣ **检查句子是否包含中文**：
        - 如果句子中包含中文，请理解中文的意思，并用合适的英语翻译替换它。

        2️⃣ **检查语法和用词错误**：
        - 逐项列出错误部分，并简要说明错误类型（如时态错误、主谓不一致、搭配错误等）。

        3️⃣ **提供正确的书面改写**：
        - 句子应符合正式英语语法，适用于书面表达。

        4️⃣ **转换为自然的口语表达**：
        - 让句子更加符合日常对话的表达方式。

        5️⃣ **分析口语句子的词伙**：
        - 逐项列出关键短语，并解释它们的用法或口语特点。
        """,
            },
            {"role": "user", "content": content},
        ]

        # 获取 DeepSeek 的回复
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        # 打印并返回模型的回复
        print(response.choices[0].message.content)
        return response.choices[0].message.content


# 使用示例
deepseek_word = DeepSeekWord()
# deepseek_word.generate_text("I is a student.")
