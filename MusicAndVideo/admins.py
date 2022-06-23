from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR, call_py
from MusicAndVideo.helpers.decorators import authorized_users_only
from MusicAndVideo.helpers.handlers import skip_current_song, skip_item
from MusicAndVideo.helpers.queues import QUEUE, clear_queue


@Client.on_message(filters.command(["بعدی"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ Tʜᴇʀᴇ's ɴᴏᴛʜɪɴɢ ɪɴ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ**")
        elif op == 1:
            await m.reply("Eᴍᴘᴛʏ ǫᴜᴇᴜᴇ  ʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**")
        else:
            await m.reply(
                f"**⏭ sᴋɪᴘ ᴘʟᴀʏʙᴀᴄᴋ** \n**🎧 ɴᴏᴡ ᴘʟᴀʏ** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ Rᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴏɴɢs ғʀᴏᴍ ᴛʜᴇ ǫᴜᴇᴜᴇ: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["پایان"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**✅ ᴇɴᴅ ᴘʟᴀʏʙᴀᴄᴋ**")
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ** \n`{e}`")
    else:
        await m.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(filters.command(["pause"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ ᴘʟᴀʏʙᴀᴄᴋ ɪs ᴘᴀᴜsᴇᴅ**\n\n• ᴛᴏ ʀᴇsᴜᴍᴇ ᴘʟᴀʏʙᴀᴄᴋ ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ » {HNDLR}ʀᴇsᴜᴍᴇ"
            )
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ** \n`{e}`")
    else:
        await m.reply("** ❌ ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ**")


@Client.on_message(filters.command(["resume"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶ ʀᴇsᴜᴍᴇᴅ ᴘᴀᴜsᴇᴅ ᴘʟᴀʏʙᴀᴄᴋ**\n\n• ᴛᴏ ᴘᴀᴜsᴇ ᴘʟᴀʏʙᴀᴄᴋ ᴜsᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ » {HNDLR}ᴘᴀᴜsᴇ**"
            )
        except Exception as e:
            await m.reply(f"**ᴇʀʀᴏʀ** \n`{e}`")
    else:
        await m.reply("**❌ ɴᴏᴛʜɪɴɢ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴘᴀᴜsᴇᴅ**")
