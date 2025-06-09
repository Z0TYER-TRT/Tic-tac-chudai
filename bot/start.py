import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import BOT_USERNAME
  
# ✅ DM /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
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

        # Keyboard
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
    else:
        await start_2(update, context)


# ✅ DM /help with 🔙 Back button
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        query = update.callback_query
        help_text = (
            "📖 *Tic Tac Toe Help*\n\n"
            "/challenge - Challenge someone to a game\n"
            "/myscore - Check your total wins and rank\n"
            "/topscore - Top 10 global players\n"
            "/topscoregroup - Top players in this group"
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
        ])

        if query:
            await query.message.edit_text(help_text, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await update.message.reply_text(help_text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await help_2(update, context)


# ✅ Group /start response
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


# ✅ Group /help with ❌ Close button
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


# ✅ Close button handler
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()
