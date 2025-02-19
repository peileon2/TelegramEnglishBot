import os
from openai import OpenAI


# Set up the API client
class QwenPlusWord:
    def __init__(self, model: str = "qwen-plus"):
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.model = model  # Set the default model name

    def generate_text(self, content):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that strictly follows instructions and always returns valid JSON output. Your task is to convert written English into natural spoken English while providing key phrase improvements."
            },
            {
                "role": "user",
                "content": (
                    "Convert the following English sentence into a more natural spoken form and return the result **strictly** in JSON format with the following structure:\n\n"
                    "{\n"
                    '  "spoken_version": "Fully revised, natural spoken version of the sentence.",\n'
                    '  "phrases": [\n'
                    "    {\n"
                    '      "original": "Original phrase from the input sentence.",\n'
                    '      "revised": "Improved, more natural spoken version."\n'
                    "    },\n"
                    "    { more entries if applicable }\n"
                    "  ]\n"
                    "}\n\n"
                    "**Rules:**\n"
                    "- **Always return valid, properly formatted JSON.**\n"
                    "- Correct spelling and grammar while preserving the original meaning.\n"
                    "- Exclude filler words like \"so,\" \"uh,\" unless they add meaning.\n"
                    "- Keep only **meaningful phrases** in the `phrases` list.\n"
                    "- Ensure the JSON output is correctly structured with no extra text or formatting issues.\n\n"
                    "Sentence: \"So uh whyd sum of my crops dry out even tho it was literally storming the day prior\""
                )
            }
        ]

        # Make the API call to the qwen-plus model
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        # Print and return the model's response
        print(response.choices[0].message.content)
        return response.choices[0].message.content


# Example usage
qwen_plus_word = QwenPlusWord()
# qwen_plus_word.generate_text("I donot know how i can 驱赶老鼠 in marry's 牧场")
