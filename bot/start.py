from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import asyncio
from config import BOT_USERNAME

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Big emoji "reaction" simulation
    await update.message.reply_text("🍓")

    # Animated emoji sequence
    emojis = ["🔮", "❄", "☃️"]
    messages = []
    for emoji in emojis:
        msg = await context.bot.send_message(chat_id, emoji)
        messages.append(msg)
        await asyncio.sleep(0.5)
    for msg in messages:
        await msg.delete()

    # Starting... message
    start_msg = await context.bot.send_message(chat_id, "<b>Starting...</b>", parse_mode="HTML")
    await asyncio.sleep(1.2)

    # Inline keyboard
    keyboard = [
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("ℹ️ Help & Commands", callback_data="help_commands")],
        [InlineKeyboardButton("📣 Support Channel", url="https://t.me/YourChannel")],
        [InlineKeyboardButton("👥 Support Chat", url="https://t.me/YourSupportChat")],
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
    await query.answer()
    await query.edit_message_text(
        "<b>🤖 Help & Commands</b>\n\n"
        "/start - Show welcome message\n"
        "/challenge [@user] - Challenge someone in a group\n\n"
        "🟢 Only works in group chats\n"
        "Players take turns by tapping the buttons.\n"
        "Turn-based game, one move at a time.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="start_back")]
        ]),
        parse_mode="HTML"
    )

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("ℹ️ Help & Commands", callback_data="help_commands")],
        [InlineKeyboardButton("📣 Support Channel", url="https://t.me/YourChannel")],
        [InlineKeyboardButton("👥 Support Chat", url="https://t.me/YourSupportChat")],
    ]
    await query.edit_message_text(
        "<b>🎮 Welcome to Tic Tac Toe Bot!</b>\n\n"
        "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
        "Challenge your friends and enjoy!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
