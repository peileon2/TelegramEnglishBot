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
        # System prompt - 描述AI助手的行为和任务
        message = {
            "role": "system",
            "content": (
                "You are an AI assistant that helps convert written English into natural spoken English. "
                "Your task is to break down the sentence into key phrases or individual words and provide "
                "a detailed comparison of each word's original and revised forms. Return the result in strict JSON format, "
                "ensuring all key phrases and words are appropriately compared. If there is no change in the word or phrase, "
                "mark it as 'unchanged'. If the word or phrase has been improved, provide the natural spoken version.\n\n"
                "JSON output structure: \n\n"
                "{\n  'spoken_version': 'The fully revised, more natural spoken version of the sentence.',\n  "
                "'phrases': [\n    {\n      'original': 'Original phrase from the input sentence.',\n      "
                "'revised': 'Revised version, making it more natural or fluent.'\n    }\n  ]\n}\n\n**Rules:**\n"
                "- Make the sentence sound as natural as possible in spoken English.\n"
                "- Break down the sentence into individual words or short phrases and compare their original and revised forms.\n"
                "- If a phrase or word is unchanged, mark it as 'unchanged'.\n"
                "- Do not change the meaning of the sentence.\n"
                "- Ensure that the revised version sounds more like natural spoken English.\n\n"
                "**Example:**\n\nInput sentence: 'I have a friend called Little Hand.'\n\nExpected output:\n"
                "{\n  'spoken_version': 'I've got a friend named Little Hand.',\n  'phrases': [\n    {\n      'original': "
                "'I have',\n      'revised': 'I've got'\n    },\n    {\n      'original': 'called',\n      'revised': "
                "'named'\n    },\n    {\n      'original': 'Little Hand',\n      'revised': 'Little Hand'  // unchanged\n"
                "  ]\n}\n\nThis example shows how the sentence is broken down and improved to sound more natural in spoken English."
            ),
        }

        # User prompt - 动态地将输入句子插入
        user_message = {"role": "user", "content": f"Sentence: '{content}'"}

        # Combine system and user prompts into messages list
        messages = [message, user_message]

        # 获取 DeepSeek 的回复
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, response_format={"type": "json_object"}
        )

        # 打印并返回模型的回复
        print(response.choices[0].message.content)
        return response.choices[0].message.content


# 使用示例
deepseek_word = DeepSeekWord()
# deepseek_word.generate_analy_content("But extra difficult fish with crown keeps appearing")
