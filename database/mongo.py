from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["tictactoe"]

user_stats = db["user_stats"]


async def update_score(user_id: int, group_id: int = None):
    """Increments score for a user globally and in the current group."""
    await user_stats.update_one(
        {"user_id": user_id},
        {"$inc": {"global_score": 1}},
        upsert=True
    )
    if group_id:
        await user_stats.update_one(
            {"user_id": user_id},
            {"$inc": {f"group_score.{str(group_id)}": 1}},
            upsert=True
        )


async def get_user_score(user_id: int, group_id: int = None):
    """Fetches the user's global and group score."""
    user = await user_stats.find_one({"user_id": user_id})
    if not user:
        return 0, 0
    global_score = user.get("global_score", 0)
    group_score = user.get("group_score", {}).get(str(group_id), 0) if group_id else 0
    return global_score, group_score


async def get_top_users(limit=10, group_id=None):
    """Returns top users globally or in a specific group."""
    if group_id:
        pipeline = [
            {"$project": {
                "user_id": 1,
                "score": {"$ifNull": [f"$group_score.{str(group_id)}", 0]}
            }},
            {"$sort": {"score": -1}},
            {"$limit": limit}
        ]
    else:
        pipeline = [
            {"$project": {"user_id": 1, "score": "$global_score"}},
            {"$sort": {"score": -1}},
            {"$limit": limit}
        ]
    return await user_stats.aggregate(pipeline).to_list(length=limit)
