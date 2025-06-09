from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
from telegram import Update
from telegram.ext import ContextTypes

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Add win count
async def add_win(user_id, username, chat_id):
    await db.scores.update_one(
        {"user_id": user_id},
        {"$inc": {"global": 1, f"group_{chat_id}": 1}, "$set": {"username": username}},
        upsert=True
    )

# Get user's score
async def get_user_score(user_id, chat_id):
    data = await db.scores.find_one({"user_id": user_id}) or {}
    return {
        "total": data.get("global", 0),
        "group": data.get(f"group_{chat_id}", 0),
        "username": data.get("username", "Unknown")
    }

# Get top total win players
async def get_top_scores_global(limit=10):
    cursor = db.scores.find().sort("global", -1).limit(limit)
    return [doc async for doc in cursor]

# Get global rank
async def get_global_rank(user_id):
    pipeline = [
        {"$setWindowFields": {
            "sortBy": {"global": -1},
            "output": {"rank": {"$rank": {}}}
        }},
        {"$match": {"user_id": user_id}},
        {"$project": {"rank": 1}}
    ]
    result = await db.scores.aggregate(pipeline).to_list(1)
    return result[0]["rank"] if result else None

# /myscore command
async def myscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    score = await get_user_score(user_id, chat_id)
    global_rank = await get_global_rank(user_id)

    await update.message.reply_text(
        f"🏅 <b>Your Score</b>\n"
        f"👤 Username: {score['username']}\n"
        f"🥇 Total Wins: <b>{score['total']}</b>\n"
        f"📊 Global Rank: <b>{global_rank or 'Unranked'}</b>",
        parse_mode="HTML"
    )

# /scoreboard command
async def topscore_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = await get_top_scores_global()
    text = "<b>🌍 Global Leaderboard (Top 10)</b>\n\n"
    for i, user in enumerate(top, 1):
        mention = f"<a href='tg://user?id={user['user_id']}'>{user.get('username', 'Unknown')}</a>"
        text += f"{i}. {mention} — {user['global']} total wins\n"

    # Show current top player
    if top:
        first = top[0]
        top_player = f"<a href='tg://user?id={first['user_id']}'>{first.get('username', 'Unknown')}</a>"
        text += f"\n🏆 <b>#1 Player:</b> {top_player} with {first['global']} total wins!"

    await update.message.reply_text(text, parse_mode="HTML")
