import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ✅ Private /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        chat_id = update.effective_chat.id
        emojis = ["🔮", "❄", "☃️"]
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
    else:
        await start_2(update, context)


# ✅ General /help entrypoint
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        if update.effective_chat.type == "private":
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="start_back")]]
            await update.message.reply_text(
                "📖 *Tic Tac Toe Help*\n\n"
                "/challenge - Challenge someone to a game\n"
                "/myscore - Check your score\n"
                "/topscore - Top global players\n"
                "/topscoregroup - Top players in this group",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await help_2(update, context)
    elif update.callback_query:
        if update.effective_chat.type == "private":
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="start_back")]]
            await update.callback_query.message.edit_text(
                "📖 *Tic Tac Toe Help*\n\n"
                "/challenge - Challenge someone to a game\n"
                "/myscore - Check your score\n"
                "/topscore - Top global players\n"
                "/topscoregroup - Top players in this group",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await help_2(update, context)


# ✅ Group /start
async def start_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Hello {update.effective_user.mention_html()}!\n\n"
        "This is a *Tic Tac Toe* game bot. You can challenge others in this group using /challenge.\n"
        "Track scores with /myscore and see who's best with /topscore!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ Help", callback_data="group_help")]
        ])
    )


# ✅ Group Help
async def help_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.edit_text(
        "📖 *Tic Tac Toe Commands:*\n\n"
        "`/challenge` - Start a game\n"
        "`/myscore` - See your total wins\n"
        "`/topscore` - Top global players\n"
        "`/topscoregroup` - Top players in this group\n"
        "`/start` - Restart welcome message",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Close", callback_data="close_help")]
        ])
    )


# ✅ Handle start_back and close_help
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if update.effective_chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("➕ ADD ME TO YOUR GROUP", url=f"https://t.me/{context.bot.username}?startgroup=true")],
            [
                InlineKeyboardButton("🤝 SUPPORT", url="https://t.me/NazkiUpdates"),
                InlineKeyboardButton("👥 SUPPORT CHAT", url="https://t.me/NazkiSupport")
            ],
            [InlineKeyboardButton("📜 COMMANDS", callback_data="help_commands")]
        ]
        await query.message.edit_text(
            "<b>🎮 Welcome back to Tic Tac Toe Bot!</b>\n\n"
            "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
            "Challenge your friends and enjoy!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
    else:
        await query.message.delete()
