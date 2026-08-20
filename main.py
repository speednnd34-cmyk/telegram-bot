import os
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# =========================
# Telegram API
# =========================

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

client = TelegramClient("my_userbot", api_id, api_hash)


# =========================
# تغيير صورة البروفايل
# الأمر: setprofile
# الاستخدام: Reply على صورة ثم اكتب setprofile
# =========================

@client.on(events.NewMessage(outgoing=True, pattern=r"^setprofile$"))
async def set_profile(event):

    reply = await event.get_reply_message()

    if not reply:
        await event.edit("❌ اعمل Reply على صورة الأول.")
        return

    if not reply.photo:
        await event.edit("❌ الرسالة اللي عملت عليها Reply مش صورة.")
        return

    file_path = None

    try:
        file_path = await reply.download_media()

        uploaded_file = await client.upload_file(file_path)

        await client(
            UploadProfilePhotoRequest(
                file=uploaded_file
            )
        )

        await event.edit("تم التغيير بنجاح! ✅")

    except Exception as e:
        await event.edit(f"❌ حصل خطأ:\n{e}")

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


# =========================
# كتم عضو
# الأمر: كتم
# الاستخدام: Reply على رسالة الشخص ثم اكتب كتم
# =========================

@client.on(events.NewMessage(outgoing=True, pattern=r"^كتم$"))
async def mute_user(event):

    reply = await event.get_reply_message()

    if not reply:
        await event.edit("❌ اعمل Reply على رسالة الشخص الأول.")
        return

    try:
        user = await reply.get_sender()

        rights = ChatBannedRights(
            until_date=None,
            send_messages=True
        )

        await client(
            EditBannedRequest(
                channel=event.chat_id,
                participant=user,
                banned_rights=rights
            )
        )

        await event.edit("تم الكتم بنجاح ✅")

    except Exception as e:
        await event.edit(f"❌ حصل خطأ:\n{e}")


# =========================
# مسح الكتم
# الأمر: مسح الكتم
# الاستخدام: Reply على رسالة الشخص ثم اكتب مسح الكتم
# =========================

@client.on(events.NewMessage(outgoing=True, pattern=r"^مسح الكتم$"))
async def unmute_user(event):

    reply = await event.get_reply_message()

    if not reply:
        await event.edit("❌ اعمل Reply على رسالة الشخص الأول.")
        return

    try:
        user = await reply.get_sender()

        rights = ChatBannedRights(
            until_date=None,
            send_messages=False
        )

        await client(
            EditBannedRequest(
                channel=event.chat_id,
                participant=user,
                banned_rights=rights
            )
        )

        await event.edit("تم مسح الكتم بنجاح ✅")

    except Exception as e:
        await event.edit(f"❌ حصل خطأ:\n{e}")


# =========================
# تشغيل الـ Userbot
# =========================

print("Userbot is running...")

client.start()

client.run_until_disconnected()
