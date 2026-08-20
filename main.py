import os
import logging
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

api_id = int(os.environ.get("API_ID", 38739119))
api_hash = os.environ.get("API_HASH", "76fd508f4878e8d77cd68e88ba65bc85")
session_str = os.environ.get("SESSION_STRING", "")

client = TelegramClient(StringSession(session_str), api_id, api_hash)

@client.on(events.NewMessage(outgoing=True))
async def main(event):
    if event.raw_text and event.raw_text.lower() == 'setprofile' and event.is_reply:
        path = None
        try:
            reply_message = await event.get_reply_message()
            if reply_message and reply_message.photo:
                path = await client.download_media(reply_message.photo)
                file = await client.upload_file(path)
                await client(functions.photos.UploadProfilePhotoRequest(file=file))
                await event.edit("تم تغيير الصورة بنجاح!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if path and os.path.exists(path):
                os.remove(path)

print("Bot is running...")
client.start()
client.run_until_disconnected()
          
