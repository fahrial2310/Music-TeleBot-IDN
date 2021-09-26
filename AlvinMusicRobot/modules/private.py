# AlvinMusicRobot (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from AlvinMusicRobot.modules.msg import Messages as tr
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import Message
from AlvinMusicRobot.config import ASSISTANT_NAME
from AlvinMusicRobot.config import PROJECT_NAME
from AlvinMusicRobot.config import SUPPORT_GRP
from AlvinMusicRobot.config import SUPPORT_MODE
from AlvinMusicRobot.config import UPDATES_CH
from AlvinMusicRobot.config import UPDATES_MODE
from AlvinMusicRobot.config import BOT_USERNAME
from AlvinMusicRobot.config import BOT_NAME
from AlvinMusicRobot.config import CREATOR_USERNAME as owner
from AlvinMusicRobot.config import OWNER_MODE as mod
from AlvinMusicRobot.config import SOURCE_CODE as git
logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.incoming & filters.command(['start']))
def _start(client, message):
    client.send_message(message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"➕ Tambahkan {BOT_NAME} Ke Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [
                    InlineKeyboardButton(
                        f"⚜️{mod}🔰", url=f"https://t.me/{owner}")
                ],[
                    InlineKeyboardButton(
                        f"🔔 {UPDATES_MODE}", url=f"https://t.me/{UPDATES_CH}"), 
                    InlineKeyboardButton(
                        f"📣 {SUPPORT_MODE}", url=f"https://t.me/{SUPPORT_GRP}")
                ],[
                    InlineKeyboardButton(
                        "🔍 Source Code 🔎", url=f"https://{git}")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
        )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        f"""**🔴 {PROJECT_NAME} sudah online**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"📣 {SUPPORT_MODE}", url=f"https://t.me/{SUPPORT_GRP}"
                    )
                ]
            ]
        ),
    )


@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    disable_web_page_preview=True
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = 'Next▶️', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        url = f"https://t.me/{SUPPORT_GRP}"
        button = [
            [InlineKeyboardButton(f"➕ Tambahkan {BOT_NAME} Ke Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text = f'🔔 {UPDATES_MODE}', url=f"https://t.me/{UPDATES_CH}"),
             InlineKeyboardButton(text = f'📣 {SUPPORT_MODE}', url=f"https://t.me/{SUPPORT_GRP}")],
            [InlineKeyboardButton(text = '🔍 Source Code 🔎', url=f"https://{git}")],
            [InlineKeyboardButton(text = '◀️Back', callback_data = f"help+{pos-1}")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '◀️Back', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = 'Next▶️', callback_data = f"help+{pos+1}")
            ],
        ]
    return button

@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""**🎵  Halo! Saya dapat memutar musik di voice chat grup dan channel telegram.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"♾ Ini Untuk Bantuan {BOT_NAME} ♾", url=f"https://t.me/{BOT_USERNAME}?start"
                    )
                ]
            ]
        ),
    )

