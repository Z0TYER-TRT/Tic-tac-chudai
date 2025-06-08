from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
from telegram import Update
from telegram.ext import ContextTypes

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def add_win(user_id, username, chat_id):
    await db.scores.update_one(
        {"user_id": user_id},
        {"$inc": {"global": 1, f"group_{chat_id}": 1}, "$set": {"username": username}},
        upsert=True
    )

async def get_user_score(user_id, chat_id):
    data = await db.scores.find_one({"user_id": user_id}) or {}
    return {
        "global": data.get("global", 0),
        "group": data.get(f"group_{chat_id}", 0)
    }

async def get_top_scores_global(limit=10):
    cursor = db.scores.find().sort("global", -1).limit(limit)
    return [doc async for doc in cursor]

async def get_top_scores_group(chat_id, limit=10):
    key = f"group_{chat_id}"
    cursor = db.scores.find({key: {"$exists": True}}).sort(key, -1).limit(limit)
    return [doc async for doc in cursor]

async def myscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = await get_user_score(update.effective_user.id, update.effective_chat.id)
    await update.message.reply_text(
        f"🏅 Your Score:\nGlobal Wins: {score['global']}\nGroup Wins: {score['group']}"
    )

async def topscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_scores_global()
    text = "🌍 Top Global Players:\n"
    for i, user in enumerate(top, 1):
        text += f"{i}. {user.get('username', 'Unknown')} — {user['global']} wins\n"
    await update.message.reply_text(text)

async def topscore_group_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_scores_group(update.effective_chat.id)
    text = "👥 Top Group Players:\n"
    for i, user in enumerate(top, 1):
        score = user.get(f"group_{update.effective_chat.id}", 0)
        text += f"{i}. {user.get('username', 'Unknown')} — {score} wins\n"
    await update.message.reply_text(text)
