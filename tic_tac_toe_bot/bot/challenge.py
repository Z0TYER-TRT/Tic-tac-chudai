from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.game import start_game

async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("⚠️ You can only challenge users in group chats.")
        return

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    elif context.args and context.args[0].startswith("@"):
        try:
            user = await context.bot.get_chat_member(update.effective_chat.id, context.args[0])
            user = user.user
        except:
            await update.message.reply_text("❌ User not found.")
            return
    else:
        await update.message.reply_text("Reply to a user or use /challenge @username")
        return

    if user.id == update.effective_user.id:
        await update.message.reply_text("🙄 You cannot challenge yourself.")
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{update.effective_user.id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{update.effective_user.id}")
        ]
    ])

    await update.message.reply_text(
        f"🎯 {user.mention_html()}, you’ve been challenged by {update.effective_user.mention_html()}!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    chat_id = query.message.chat_id

    if data.startswith("confirm_"):
        challenger_id = int(data.split("_")[1])
        if user.id == challenger_id:
            await query.answer("❌ Only the challenged user can confirm.")
            return
        await query.edit_message_text("✅ Challenge accepted! Starting game...")
        challenger = await context.bot.get_chat_member(chat_id, challenger_id)
        await start_game(update, context, challenger.user, user)

    elif data.startswith("cancel_"):
        challenger_id = int(data.split("_")[1])
        if user.id != challenger_id:
            await query.edit_message_text("🚫 Challenge was declined.")
        else:
            await query.answer("❌ You cannot cancel your own challenge.")
