import pyrogram
import logging
import json, requests, os, shlex, asyncio, uuid, shutil
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
from configs import Config
from pyrogram.errors import UserNotParticipant
from pyrogram.errors import UserBannedInChannel
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied
from database.sql import add_user, query_msg
from database.support import users_info
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
downloads = './downloads/{}/'

#DL_BUTTONS

FORCE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('JOIN HERE 🔖', url=f"https://t.me/codexbotz")
        ]]
    )        

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤔Hᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('🤖Aʙᴏᴜᴛ', callback_data='about')],
        [InlineKeyboardButton('🔒Cʟᴏsᴇ', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤖Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('🔒Cʟᴏsᴇ', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤔Hᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('🔒Cʟᴏsᴇ', callback_data='close')
        ]]
    )
    
DL_BUTTONS=[
    [
        InlineKeyboardButton('video 📹', callback_data='nowm'),
        InlineKeyboardButton('Audio🎶', callback_data='audio'),
    ],
]

SU_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Code 𝕏 Botz', url='https://t.me/CodeXBotz')],
        [InlineKeyboardButton('Rate this Bot ⭐️', url='https://t.me/CodeXBotz')
        ]]
    )


START_TEXT = """<b>Hi, {}</b>\n
<b>I am a TikTok Downloader bot.</b>
<b>you can download tiktok videos without watermark and audios.</b>
"""

HELP_TEXT = """**❔ How to use this Bot**

🔷 Just send me url of a post and i will download and send the file of it
"""

ABOUT_TEXT = """**ABOUT ME**

 **Language:** [Python 3](https://www.python.org/)
 **Libary :** [pyrogram](https://github.com/pyrogram/pyrogram)
 **Channel:** [Code 𝕏 Botz](https://t.me/CodeXBotz)
 **Support:** [Code 𝕏 Botz Support](https://t.me/CodeXBotzSupport)
"""
FORCE_TEXT ="""You need to join @CodeXBotz in order to use this bot.\nSo please join channel and enjoy bot\n\n**Press the Following Button to join Now 👇**
"""
USERS_LIST = "<b>⭕️Total:</b>\n\n⭕️Subscribers - {}\n⭕️Blocked- {}"
WAIT_MSG = "<b>Processing ...</b>"
REPLY_ERROR = "<code>Use this command as a replay to any telegram message with out any spaces.</code>"
DOWN_MSG = "**downloading... 📥**"
# Running bot
bot = Client('TikTokDL', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
  args = shlex.split(cmd)
  process = await asyncio.create_subprocess_exec(
      *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  return (
      stdout.decode("utf-8", "replace").strip(),
      stderr.decode("utf-8", "replace").strip(),
      process.returncode,
      process.pid,
  )
  
@bot.on_message(filters.private & filters.command(["us"]))
async def subscribers_count(bot, m: Message):
    msg = await m.reply_text(WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]
    await m.delete()
    await msg.edit(USERS_LIST.format(active, blocked))


@bot.on_message(filters.private & filters.command(["xat"]))
async def send_text(bot, update):
    if update.reply_to_message:
        query = await query_msg()
        broadcast_msg = update.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await update.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for row in query:
            chat_id = int(row[0])
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>
Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await update.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# Start
@bot.on_message(filters.private & filters.command(["start"]))
async def _start(bot, update):
    id = update.from_user.id
    user_name = '@' + update.from_user.username if update.from_user.username else None
    await add_user(id, user_name)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )  

@bot.on_message(filters.private & filters.command(["about"]))
async def about_handler(bot, message):
    await message.reply_text(
        text=ABOUT_TEXT,
        parse_mode="markdown",
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )

@bot.on_message(filters.private & filters.command(["xdevs"]))
async def about_handler(bot, message):
    await message.reply_text(
        text="broadcast = /xat\nusers = /us",
        parse_mode="markdown",
        disable_web_page_preview=True
    )
    
@bot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode="markdown",
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
    )

# Downloader for tiktok
@bot.on_message(filters.regex(pattern='.*http.*') & filters.private)
async def _tiktok(bot, update):
    if Config.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Config.UPDATES_CHANNEL, update.chat.id)
            if user.status == "kicked":
                return await bot.send_message(
                    chat_id=update.chat.id,
                    text="you are banned\n\n  **contact @codexbotzsupport **",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                
        except UserNotParticipant:
            return await bot.send_message(
                chat_id=update.chat.id,
                text=FORCE_TEXT,
                reply_markup=FORCE_BUTTON,
                parse_mode="markdown")
         
        except Exception:
            return await bot.send_message(
                chat_id=update.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ** @codexbotzsupport",
                parse_mode="markdown",
                disable_web_page_preview=True
            )

    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    test = "**choose your options**"
    if not 'tiktok.com' in resp.url:
        return
    await update.reply_animation("mp4.mp4", caption=test,
      reply_markup=InlineKeyboardMarkup(DL_BUTTONS))

# _callbacks
@bot.on_callback_query()
async def _callbacks(bot, cb: CallbackQuery):
  if cb.data == 'nowm':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.edit("`pleasewait...`")
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if '?' in resp.url:
        tt = resp.url.split('?', 1)[0]
    else:
        tt = resp.url
    ttid = dirs+tt.split('/')[-1]
    r = requests.get('https://api.reiyuura.me/api/dl/tiktok?url='+tt)
    result = r.text
    rs = json.loads(result)
    link = rs['result']['nowm']
    resp = session.head(link, allow_redirects=True)
    r = requests.get(resp.url, allow_redirects=True)
    open(f'{ttid}.mp4', 'wb').write(r.content)
    file = f"{ttid}.mp4"
    cap = "thanks"
    await bot.send_video(update.chat.id, video=file, caption=cap, reply_markup=SU_BUTTONS)
    await cb.message.delete()
    os.remove(file)
    shutil.rmtree(dirs)
  elif cb.data == 'audio':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.edit("`pleasewait....`")
    url = update.text
    session = requests.Session()
    resp = session.head(url, allow_redirects=True)
    if '?' in resp.url:
        tt = resp.url.split('?', 1)[0]
    else:
        tt = resp.url
    ttid = dirs+tt.split('/')[-1]
    r = requests.get('https://api.reiyuura.me/api/dl/tiktok?url='+tt)
    result = r.text
    rs = json.loads(result)
    link = rs['result']['wm']
    resp = session.head(link, allow_redirects=True)
    r = requests.get(resp.url, allow_redirects=True)
    open(f'{ttid}.mp4', 'wb').write(r.content)
    cmd = f'ffmpeg -i "{ttid}.mp4" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "{ttid}.mp3"'
    file = f"{ttid}.mp3"
    cap = "thanks"
    await run_cmd(cmd)
    await bot.send_audio(update.chat.id, audio=file, caption=cap, reply_markup=SU_BUTTONS)
    await cb.message.delete()
    os.remove(file)
    shutil.rmtree(dirs)
  elif cb.data == "help":
    await cb.message.edit_text(
      text=HELP_TEXT,
      disable_web_page_preview=True,
      reply_markup=HELP_BUTTONS
      )
  elif cb.data == "about":
    await cb.message.edit_text(
      text=ABOUT_TEXT,
      disable_web_page_preview=True,
      reply_markup=ABOUT_BUTTONS
      )  
  elif cb.data == 'close':
    await cb.message.delete()
    
bot.run()
    