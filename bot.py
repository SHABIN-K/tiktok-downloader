import json, requests, os, shlex, asyncio, uuid, shutil
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Configs
API_HASH = os.environ['API_HASH']
APP_ID = int(os.environ['APP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
downloads = './downloads/{}/'

#DL_BUTTONS

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

START_TEXT = """Hi {},
I Am A Powerfull
"""

HELP_TEXT = """helo"""

ABOUT_TEXT = """**ABOUT ME**
 **Language:** [Python 3](https://www.python.org/)
 **Libary :** [pyrogram](https://github.com/pyrogram/pyrogram)
 **Channel:** [Code 𝕏 Botz](https://t.me/CodeXBotz)
 **Support:** [Code 𝕏 Botz Support](https://t.me/CodeXBotzSupport)
"""
USERS_LIST = "<b>⭕️Total:</b>\n\n⭕️Subscribers - {}\n⭕️Blocked- {}"
WAIT_MSG = "<b>Processing ...</b>"
REPLY_ERROR = "<code>Use this command as a replay to any telegram message with out any spaces.</code>"

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

# Start
@bot.on_message(filters.private & filters.command(["start"]))
async def _start(bot, update):
    await update.reply_text(
        text=START_TEXT,
        parse_mode="markdown",
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
  url = update.text
  session = requests.Session()
  resp = session.head(url, allow_redirects=True)
  if not 'tiktok.com' in resp.url:
    return
  await update.reply('Select the options below', True, reply_markup=InlineKeyboardMarkup(DL_BUTTONS))

# _callbacks

@bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()

@bot.on_callback_query()
async def _callbacks(bot, cb: CallbackQuery):
  if cb.data == 'nowm':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.delete()
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
    await bot.send_video(update.chat.id, f'{ttid}.mp4',)
    shutil.rmtree(dirs)
  elif cb.data == 'audio':
    dirs = downloads.format(uuid.uuid4().hex)
    os.makedirs(dirs)
    cbb = cb
    update = cbb.message.reply_to_message
    await cb.message.delete()
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
    await run_cmd(cmd)
    await bot.send_audio(update.chat.id, f'{ttid}.mp3',)
    shutil.rmtree(dirs)

bot.run()