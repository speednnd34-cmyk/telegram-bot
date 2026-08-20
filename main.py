from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

# البيانات الخاصة بك
api_id = 38739119 
api_hash = "76fd508f4878e8d77cd68e88ba65bc85"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# 1. أمر تغيير صورة البروفايل عند الرد على صورة
@app.on_message(filters.me & filters.command("setprofile", prefixes="."))
async def set_profile_photo(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.edit_text("❌ **يرجى الرد على صورة لتغيير البروفايل!**")
        return

    photo_path = await client.download_media(message.reply_to_message.photo)
    await client.set_profile_photo(photo=photo_path)
    await message.edit_text("تم تغيير الصورة بنجاح!")

# 2. أمر كتم الشخص محلياً
muted_users = set()

@app.on_message(filters.me & filters.command("كتم", prefixes="."))
async def mute_user(client, message):
    if not message.reply_to_message:
        await message.edit_text("❌ **يرجى الرد على الشخص المراد كتمه!**")
        return

    target_user_id = message.reply_to_message.from_user.id
    try:
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=target_user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
    except Exception:
        pass
    muted_users.add(target_user_id)
    await message.edit_text("✅ **تم كتم الشخص بنجاح!**")

@app.on_message(filters.group & ~filters.me)
async def delete_muted_messages(client, message):
    if message.from_user and message.from_user.id in muted_users:
        try:
            await message.delete()
        except Exception:
            pass
            
app.run()
