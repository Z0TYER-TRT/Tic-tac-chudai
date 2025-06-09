import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes

# 🎯 DM Start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        await start_2(update, context)
        return

    args = context.args
    if args and args[0] == "help":
        await help_callback(update, context)
        return

    chat_id = update.effective_chat.id
    emojis = ["🔮"]
    for emoji in emojis:
        msg = await context.bot.send_message(chat_id, emoji)
        await asyncio.sleep(0.3)
        await msg.delete()

    start_msg = await context.bot.send_message(chat_id, "<b>Starting...</b>", parse_mode="HTML")
    await asyncio.sleep(1)

    keyboard = [
        [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=f"https://t.me/{context.bot.username}?startgroup=true")],
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


# 🆘 DM Help
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        msg = update.message
    elif update.callback_query:
        msg = update.callback_query.message
    else:
        return

    await msg.reply_text(
        "📖 *Tic Tac Toe Help*\n\n"
        "/challenge - Challenge someone to a game\n"
        "/myscore - Check your score\n"
        "/topscore - Global top players\n"
        "/topscoregroup - Top players in this group",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
        ])
    )


# 🆘 /help handler
async def help_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await help_dm(update, context)
    else:
        bot_username = context.bot.username
        await update.message.reply_text(
            "ℹ️ Help is available in my DM.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📨 Open Help Menu", url=f"https://t.me/{bot_username}?start=help")]
            ])
        )


# 🟢 Group /start
async def start_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Hello {update.effective_user.mention_html()}!\n\n"
        "*This is a Tic Tac Toe game bot.*\n"
        "Use `/challenge` to challenge others in this group.\n"
        "Check your score with `/myscore` or see the best players with `/topscore`.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ Help", callback_data="group_help")]
        ])
    )


# 🟢 Group Help (from start_2 Help button)
async def help_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return  # ignore if no button press

    keyboard = [
        [InlineKeyboardButton("Close", callback_data="close_help")]
    ]

    await query.message.edit_text(
        "📖 <b>Tic Tac Toe Help</b>\n\n"
        "/challenge - Challenge someone to a game\n"
        "/myscore - Check your score\n"
        "/topscore - Global top players\n"
        "/topscoregroup - Top players in this group",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
                       )


# 🔙 Back Button in DM (no emoji animation)
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [
            InlineKeyboardButton("🤝 SUPPORT", url="https://t.me/NazkiUpdates"),
            InlineKeyboardButton("👥 SUPPORT CHAT", url="https://t.me/NazkiSupport")
        ],
        [InlineKeyboardButton("📜 COMMANDS", callback_data="help_commands")]
    ]

    await query.message.edit_text(
        "<b>🎮 Welcome to Tic Tac Toe Bot!</b>\n\n"
        "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
        "Challenge your friends and enjoy!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
