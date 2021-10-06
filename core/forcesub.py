import asyncio
from vars import Configs
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


async def ForceSub(bot: Client, event: Message):

    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(Configs.UPDATES_CHANNEL) if Configs.UPDATES_CHANNEL.startswith("-100") else Configs.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to codexbotz\n\nError: {err}")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(Configs.UPDATES_CHANNEL) if Configs.UPDATES_CHANNEL.startswith("-100") else Configs.UPDATES_CHANNEL), user_id=event.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Sorry Sir, You are Banned Contact my [Support Group](https://t.me/codexbotzsupport)",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=event.message_id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=event.from_user.id,
            text="You need to join @CodeXBotz in order to use this bot.\n**Press the Following Button to join Now 👇**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Code 𝕏 Botz", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=event.message_id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, event)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}")
        return 200