from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
from telegram import Update
from telegram.ext import ContextTypes

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def add_win(user_id, username, chat_id):
    await db.scores.update_one(
        {"user_id": user_id},
        {
            "$inc": {"total_wins": 1, f"group_{chat_id}": 1},
            "$set": {"username": username}
        },
        upsert=True
    )

async def get_user_data(user_id):
    return await db.scores.find_one({"user_id": user_id}) or {}

async def get_global_rank(user_id):
    pipeline = [
        {"$sort": {"total_wins": -1}},
        {"$project": {"user_id": 1}},
    ]
    cursor = db.scores.aggregate(pipeline)
    rank = 1
    async for user in cursor:
        if user["user_id"] == user_id:
            return rank
        rank += 1
    return None  # If not found

async def get_top_scores(limit=10):
    cursor = db.scores.find().sort("total_wins", -1).limit(limit)
    return [doc async for doc in cursor]

async def myscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    user_data = await get_user_data(user_id)
    total_wins = user_data.get("total_wins", 0)
    username = user_data.get("username") or user.username or user.first_name
    rank = await get_global_rank(user_id)

    rank_text = f"{rank}" if rank else "Unranked"

    mention = f"<a href='tg://user?id={user_id}'>{username}</a>"

    await update.message.reply_text(
        f"🎖 <b>Your Score</b>\n\n"
        f"👤 Username: {mention}\n"
        f"🏆 Total Wins: <b>{total_wins}</b>\n"
        f"📊 Global Rank: <b>{rank_text}</b>",
        parse_mode="HTML"
    )

async def topscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_scores()
    text = "<b>🌍 Global Leaderboard (Top 10)</b>\n\n"
    for i, user in enumerate(top, 1):
        username = user.get("username", "Unknown")
        wins = user.get("total_wins", 0)
        mention = f"<a href='tg://user?id={user['user_id']}'>{username}</a>"
        text += f"{i}. {mention} — {wins} wins\n"

    await update.message.reply_text(text, parse_mode="HTML")
