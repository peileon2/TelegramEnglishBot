from openai import OpenAI
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY 环境变量未设置！")


class DeepSeekWord:
    def __init__(self, model: str = "deepseek-chat"):
        # 初始化 DeepSeek 客户端
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com"
        )
        self.model = model  # 设置默认的模型名称

    def generate_analy_content(self, content):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that strictly follows instructions and always returns valid JSON output. Your task is to convert written English into natural spoken English while providing key phrase improvements."
            },
            {
                "role": "user",
                "content": (
                    "Convert the following English sentence into a **more natural spoken form** and return the result **strictly** in JSON format with this structure:\n\n"
                    "{\n"
                    '  "spoken_version": "Fully revised, more natural spoken version of the sentence.",\n'
                    '  "phrases": [\n'
                    "    {\n"
                    '      "original": "Original phrase from the input sentence.",\n'
                    '      "revised": "Improved, more natural spoken version."\n'
                    "    }\n"
                    "    // Add more entries as needed, if no change is needed, mark as 'unchanged'.\n"
                    "  ]\n"
                    "}\n\n"
                    "**Rules:**\n"
                    "- **Always return valid, properly formatted JSON.**\n"
                    "- **Make the sentence sound as natural as possible in spoken English.**\n"
                    "- **DO NOT simply replace words—adjust the phrasing to be natural.**\n"
                    "- **Keep 'phrases' meaningful—don't force changes if unnecessary.**\n"
                    "- **If a phrase is already natural, mark it as 'unchanged'.**\n"
                    "- **DO NOT change the meaning of the sentence.**\n\n"
                    f"Sentence: \"{content}\""
                )
            }
        ]




        # 获取 DeepSeek 的回复
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={
            'type': 'json_object'
        }
        )

        # 打印并返回模型的回复
        print(response.choices[0].message.content)
        return response.choices[0].message.content


# 使用示例
deepseek_word = DeepSeekWord()
deepseek_word.generate_analy_content("But extra difficult fish with crown keeps appearing")
