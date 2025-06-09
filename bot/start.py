import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from config import BOT_USERNAME


# ✅ /start handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == "private":
        # Animated emojis
        emojis = ["🔮"]
        for emoji in emojis:
            msg = await context.bot.send_message(chat.id, emoji)
            await asyncio.sleep(0.3)
            await msg.delete()

        # Send "Starting..." msg
        start_msg = await context.bot.send_message(chat.id, "<b>Starting...</b>", parse_mode="HTML")
        await asyncio.sleep(1)

        # Inline keyboard
        keyboard = [
            [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("🤝 Channel", url="https://t.me/NazkiUpdates"),
                InlineKeyboardButton("👥 Support Chat", url="https://t.me/NazkiSupport")
            ],
            [InlineKeyboardButton("📜 Help & Command", callback_data="help_commands")]
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


# ✅ DM help menu (callback_data="help_commands")
async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        query = update.callback_query
        if query:
            await query.message.edit_text(
                "<b>📖 Tic Tac Toe Help</b>\n\n"
                "<code>/challenge</code> - Challenge someone to a game\n"
                "<code>/myscore</code> - Check your score\n"
                "<code>/topscore</code> - Global top players\n"
                "<code>/topscoregroup</code> - Top players in this group",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
                ])
            )
        else:
            # Handle /help command (in DM)
            await context.bot.send_message(
                chat.id,
                "<b>📖 Tic Tac Toe Help</b>\n\n"
                "<code>/challenge</code> - Challenge someone to a game\n"
                "<code>/myscore</code> - Check your score\n"
                "<code>/topscore</code> - Global top players\n"
                "<code>/topscoregroup</code> - Top players in this group",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
                ])
            )
    else:
        # Group help: show redirect button to bot
        await update.message.reply_text(
            "ℹ️ Please click the button below to open the help menu in DM.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📬 Open Help in Bot", url=f"https://t.me/{BOT_USERNAME}?start=help")]
            ])
        )


# ✅ Back from help to start (edit same msg)
async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("➕ Add Me To Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("🤝 Channel", url="https://t.me/NazkiUpdates"),
            InlineKeyboardButton("👥 Support Chat", url="https://t.me/NazkiSupport")
        ],
        [InlineKeyboardButton("📜 Help & Command", callback_data="help_commands")]
    ]
    await query.message.edit_text(
        "<b>🎮 Welcome to Tic Tac Toe Bot!</b>\n\n"
        "Play 1v1 Tic Tac Toe using inline buttons in group chats.\n"
        "Challenge your friends and enjoy!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# ✅ /start in group
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


# ✅ Group-specific help callback (used by start_2)
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


# ✅ Close help (delete group help msg)
async def close_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()
