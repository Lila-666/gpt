import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from openai import AsyncOpenAI
from config import API_ID, API_HASH, SESSION_STRING, OPENAI_API_KEY

app = Client(
    "ai-userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

ai = AsyncOpenAI(api_key=OPENAI_API_KEY)

auto_reply = True

SYSTEM_PROMPT = """
Kamu adalah manusia asli yang sedang chatting di Telegram.

Balas dengan gaya santai, natural, pendek, dan realistis seperti anak muda Indonesia.

Kadang boleh pakai:
- wkwk
- 😭
- bjir
- lah
- anjir
- awokwok

Jangan terlalu formal.
Jangan menjelaskan panjang lebar kecuali ditanya serius.

PENTING:
- Jangan pernah mengatakan bahwa kamu AI, bot, assistant, atau program.
- Jangan pernah mengaku menggunakan OpenAI, ChatGPT, atau teknologi AI.
- Jika ditanya apakah kamu bot/AI, jawab seperti manusia biasa dan alihkan topik dengan natural.
- Jangan gunakan gaya customer service.
- Balas seolah akun Telegram pribadi manusia sungguhan.
"""

@app.on_message(filters.me & filters.command("aion", prefixes="."))
async def ai_on(client, message):
    global auto_reply
    auto_reply = True
    await message.reply("AI aktif ✅")

@app.on_message(filters.me & filters.command("aioff", prefixes="."))
async def ai_off(client, message):
    global auto_reply
    auto_reply = False
    await message.reply("AI mati ❌")

@app.on_message(filters.private & ~filters.me)
async def auto_ai_reply(client, message):

    global auto_reply

    if not auto_reply:
        return

    if not message.text:
        return

    text = message.text.strip()

    if len(text) < 2:
        return

    try:

        # delay natural
        await asyncio.sleep(random.randint(3, 9))

        # typing
        await client.send_chat_action(
            message.chat.id,
            ChatAction.TYPING
        )

        response = await ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.9,
            max_tokens=120
        )

        reply = response.choices[0].message.content.strip()

        # anti kosong
        if not reply:
            return

        await message.reply(reply)

    except Exception as e:
        print(f"ERROR: {e}")

print("AI USERBOT AKTIF 🔥")

app.run()
