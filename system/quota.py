#!/usr/bin/env python3
from bot.helper.ext_utils.db_handler import DbManger
from datetime import datetime

async def check_quota(user_id, daily_limit):
    db = DbManger()
    user_stats = await db.get_user_stats(user_id)
    if not user_stats:
        await db.update_user_stats(user_id, {"daily_used": 0, "last_reset": datetime.now()})
        return True

    daily_used = user_stats.get('daily_used', 0)
    last_reset = user_stats.get('last_reset')

    if last_reset and last_reset.date() < datetime.now().date():
        daily_used = 0
        await db.update_user_stats(user_id, {"daily_used": 0, "last_reset": datetime.now()})

    return daily_used < daily_limit

async def update_quota(user_id, amount=1):
    db = DbManger()
    user_stats = await db.get_user_stats(user_id)
    daily_used = user_stats.get('daily_used', 0) if user_stats else 0
    await db.update_user_stats(user_id, {"daily_used": daily_used + amount, "last_reset": datetime.now()})
