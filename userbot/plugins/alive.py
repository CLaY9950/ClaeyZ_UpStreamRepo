import random
import re
import time
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  😆 "
    CUSTOM_ALIVE_TEXT = (
        gvarstatus("ALIVE_TEXT") or "**𝚈𝚘 𝙸'𝚖 𝚁𝚞𝚗𝚗𝚒𝚗𝙶 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚈 😗**"
    )
    CAT_IMG = gvarstatus("ALIVE_PIC")
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        A_IMG = list(CAT)
        PIC = random.choice(A_IMG)
        cat_caption = f"{CUSTOM_ALIVE_TEXT}\n\n"
        cat_caption += f"**{EMOJI} 🖥ᴅᴀᴛᴀʙᴀsᴇ :** `{check_sgnirts}`\n"
        cat_caption += f"**{EMOJI} 📃ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version.__version__}\n`"
        cat_caption += f"**{EMOJI} 📋ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `{catversion}`\n"
        cat_caption += f"**{EMOJI} 📘ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{python_version()}\n`"
        cat_caption += f"**{EMOJI} 🧿ᴜᴘᴛɪᴍᴇ :** `{uptime}\n`"
        cat_caption += f"**{EMOJI} 👨🏼‍💻ᴍᴀsᴛᴇʀ:** {mention}\n"
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=cat_caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            f"{CUSTOM_ALIVE_TEXT}\n\n"
            f"**{EMOJI} 🖥ᴅᴀᴛᴀʙᴀsᴇ :** `{check_sgnirts}`\n"
            f"**{EMOJI} 📃ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version.__version__}\n`"
            f"**{EMOJI} 📋ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `{catversion}`\n"
            f"**{EMOJI} 📘ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{python_version()}\n`"
            f"**{EMOJI} 🧿ᴜᴘᴛɪᴍᴇ :** `{uptime}\n`"
            f"**{EMOJI} 👨🏼‍💻ᴍᴀsᴛᴇʀ:** {mention}\n",
        )


@catub.cat_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ✥ "
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**Catuserbot is Up and Running**"
    cat_caption = f"{CUSTOM_ALIVE_TEXT}\n"
    cat_caption += f"**{EMOJI} 📃ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version.__version__}\n`"
    cat_caption += f"**{EMOJI} 📋ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `{catversion}`\n"
    cat_caption += f"**{EMOJI} 📘ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{python_version()}\n`"
    cat_caption += f"**{EMOJI} 👨🏼‍💻ᴍᴀsᴛᴇʀ:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
