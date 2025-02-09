from fastapi import FastAPI, Request, HTTPException
import os
import httpx
import uvicorn
from dotenv import load_dotenv
from telegramenglishteacher.zhipuWord import zhipuWord

app = FastAPI()

load_dotenv()  # 读取 .env 文件

SECRET_WEBHOOK_TOKEN = os.getenv("SECRET_WEBHOOK_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    # 获取请求头中的 Token
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")

    # 验证 Token
    if secret_token != SECRET_WEBHOOK_TOKEN:
        # 调试信息：打印 `repr()` 来检查实际字符
        print(f"secret_token: {repr(secret_token)}")
        print(f"SECRET_WEBHOOK_TOKEN: {repr(SECRET_WEBHOOK_TOKEN)}")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret token")

    # 解析 JSON 数据
    update = await request.json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]

        if "text" in message:
            return await handle_text_message(chat_id, message["text"])
        elif "photo" in message:
            return await handle_photo_message(chat_id)
        elif "document" in message:
            return await handle_document_message(chat_id)

    return {"ok": True}


# 处理文本消息
async def handle_text_message(chat_id, text):
    reply_text = zhipuWord.generate_text(text)
    await send_message(chat_id, reply_text)
    return {"ok": True}


# 处理图片消息
async def handle_photo_message(chat_id):
    await send_message(chat_id, "收到图片，但我暂时无法处理 🖼️")
    return {"ok": True}


# 处理文档消息
async def handle_document_message(chat_id):
    await send_message(chat_id, "收到文件，感谢你的上传 📄")
    return {"ok": True}


# 发送 Telegram 消息（异步）
async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()  # 检查 HTTP 请求是否成功
        except httpx.HTTPStatusError as e:
            print(f"Telegram API 错误: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"发送消息失败: {str(e)}")


# Cloud Run 需要监听 0.0.0.0:$PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # 默认 8080，但应确保 Cloud Run 传入了 PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
