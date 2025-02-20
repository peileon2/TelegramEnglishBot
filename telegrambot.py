from fastapi import FastAPI, BackgroundTasks
import os
import httpx
from dotenv import load_dotenv
import json

# 导入外部模块
from telegramenglishteacher.Talkfirst import qwen_plus_word
from telegramenglishteacher.deepseekword import deepseek_word

app = FastAPI()

load_dotenv()  # 读取 .env 文件

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class TelegramBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def send_message(self, chat_id: int, text: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()  # 检查 HTTP 请求是否成功
            except httpx.HTTPStatusError as e:
                print(
                    f"Telegram API 错误: {e.response.status_code} - {e.response.text}"
                )
            except Exception as e:
                print(f"发送消息失败: {str(e)}")

    async def send_voice(self, chat_id: int, voice_file: str, caption: str = None):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendVoice"
        payload = {"chat_id": chat_id}
        files = {"voice": open(voice_file, "rb")}

        if caption:
            payload["caption"] = caption

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, data=payload, files=files)
                response.raise_for_status()  # 检查 HTTP 请求是否成功
            except httpx.HTTPStatusError as e:
                print(
                    f"Telegram API 错误: {e.response.status_code} - {e.response.text}"
                )
            except Exception as e:
                print(f"发送语音消息失败: {str(e)}")
            finally:
                files["voice"].close()  # 确保文件被关闭

    def json_to_markdown(self, data):
        markdown = "## Phrases\n\n"
        markdown += "| Original Phrase                   | Revised Phrase                        | 查看对比                    |\n"
        markdown += "|------------------------------------|---------------------------------------|----------------------------|\n"

        for phrase in data["phrases"]:
            original = phrase["original"]
            revised = phrase["revised"]
            # 创建查看对比的超链接
            comparison = f"[{original} vs {revised}](https://www.deepseek.com/)"
            markdown += f"| {original} | {revised} | {comparison} |\n"

        return markdown

    async def send_markdown(self, chat_id, text):
        ## tran json into markdown
        reply_json = deepseek_word.generate_analy_content(text)
        reply_markdwon = self.json_to_markdown(data=json.loads(reply_json))
        print(reply_markdwon)
        await self.send_message(chat_id, reply_markdwon)

    async def handle_text_message(self, chat_id, text):
        reply_text = qwen_plus_word.generate_text(text)
        await self.send_message(chat_id, reply_text)
        return reply_text

    async def handle_photo_message(self, chat_id):
        await self.send_message(chat_id, "收到图片，但我暂时无法处理 🖼️")

    async def handle_document_message(self, chat_id):
        await self.send_message(chat_id, "收到文件，感谢你的上传 📄")


# 创建 TelegramBot 实例
bot = TelegramBot(TELEGRAM_BOT_TOKEN)
