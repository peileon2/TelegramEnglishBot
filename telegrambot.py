from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import os
import httpx
import uvicorn
from dotenv import load_dotenv

# 导入外部模块
from telegramenglishteacher.Talkfirst import qwen_plus_word
from telegramenglishteacher.deepseekword import deepseek_word

app = FastAPI()

load_dotenv()  # 读取 .env 文件

SECRET_WEBHOOK_TOKEN = os.getenv("SECRET_WEBHOOK_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class TelegramBot:
    def __init__(self, bot_token: str, secret_token: str):
        self.bot_token = bot_token
        self.secret_token = secret_token

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

    async def handle_text_message(
        self, chat_id, text, background_tasks: BackgroundTasks
    ):
        reply_text = qwen_plus_word.generate_text(text)
        background_tasks.add_task(deepseek_word.generate_analy_content, text)
        await self.send_message(chat_id, reply_text)

    async def handle_photo_message(self, chat_id):
        await self.send_message(chat_id, "收到图片，但我暂时无法处理 🖼️")

    async def handle_document_message(self, chat_id):
        await self.send_message(chat_id, "收到文件，感谢你的上传 📄")


# 创建 TelegramBot 实例
bot = TelegramBot(TELEGRAM_BOT_TOKEN, SECRET_WEBHOOK_TOKEN)
