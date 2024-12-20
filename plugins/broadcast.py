import datetime, time, os, asyncio,logging 
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton
from pyrogram import Client, filters, enums
from database.users_chats_db import db


@Client.on_message(filters.command("broadcast") & filters.user(int(5585035853)) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text('Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs...')
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"Bʀᴏᴀᴅᴄᴀsᴛ Iɴ Pʀᴏɢʀᴇss:\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await bot.send_message(message.chat.id, f"Bʀᴏᴀᴅᴄᴀsᴛ Coᴍᴩʟᴇᴛᴇᴅ:\nTɪᴍᴇ Tᴀᴋᴇᴅ{time_taken} Sᴇᴄ\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ: {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSucᴄᴇꜱꜱ: {success}\nBʟᴏᴄᴋᴇᴅ: {blocked}\nDᴇʟᴇᴛᴇᴅ: {deleted}")

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"