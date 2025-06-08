from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import asyncio
from config import BOT_USERNAME

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Emoji animation
    emojis = ["🔮", "❄", "☃️"]
    for emoji in emojis:
        msg = await context.bot.send_message(chat_id, emoji)
        await asyncio.sleep(0.3)
        await msg.delete()

    # Starting message
    start_msg = await context.bot.send_message(chat_id, "<b>Starting...</b>", parse_mode="HTML")
    await asyncio.sleep(1)

    # Main keyboard layout
    keyboard = [
        [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("🤝 SUPPORT", url="https://t.me/NazkiUpdates"),
            InlineKeyboardButton("👥 SUPPORT CHAT", url="https://t.me/NazkiSupport")
        ],
        [InlineKeyboardButton("📜 COMMANDS", callback_data="help_commands")]
    ]

    await start_msg.edit_text(
        "<b>🎮 Welcome to Tic Tac Toe Bot!</b>\n\n"
        "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
        "Challenge your friends and enjoy!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    help_text = (
        "<b>🤖 Help & Commands</b>\n\n"
        "/start - Show welcome message\n"
        "/help - Show this help panel\n"
        "/challenge [@user] - Challenge someone in a group\n"
        "/myscore - View your score\n"
        "/scoreboard - View group/global top players\n\n"
        "📌 How To Play:\n"
        "- Use /challenge by replying to a user or mention them\n"
        "- Only the challenged user can confirm\n"
        "- Play by clicking inline buttons (X/O)\n"
        "- Scores are tracked globally and per group\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="start_back")]
    ])

    if query:
        await query.answer()
        await query.edit_message_text(help_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await update.message.reply_text(help_text, reply_markup=keyboard, parse_mode="HTML")


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("🤝 SUPPORT", url="https://t.me/NazkiUpdates"),
            InlineKeyboardButton("👥 SUPPORT CHAT", url="https://t.me/NazkiSupport")
        ],
        [InlineKeyboardButton("📜 COMMANDS", callback_data="help_commands")]
    ]

    await query.edit_message_text(
        "<b>🎮 Welcome to Tic Tac Toe Bot!</b>\n\n"
        "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
        "Challenge your friends and enjoy!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
