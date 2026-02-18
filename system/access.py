#!/usr/bin/env python3
from bot import OWNER_ID, user_data, config_dict
from bot.helper.ext_utils.db_handler import DbManger
from subscription.plans import plans
from datetime import datetime

async def check_user_access(user_id):
    res = {
        "is_owner": False,
        "is_admin": False,
        "is_premium": False,
        "is_expired": False,
        "unlimited": False,
        "daily_remaining": 0,
        "priority_queue": False
    }

    db = DbManger()

    # 1. Check Owner
    if user_id == OWNER_ID:
        res["is_owner"] = True
        res["unlimited"] = True
        res["priority_queue"] = True
        res["daily_remaining"] = 999
        return res

    # 2. Check Admin (Sudo)
    if user_id in user_data and user_data[user_id].get('is_sudo'):
        res["is_admin"] = True
        res["is_premium"] = True # Admin shows premium badge
        res["unlimited"] = True
        res["priority_queue"] = True
        res["daily_remaining"] = 999
        return res

    # 3. Check Premium
    premium_record = await db.get_premium_data(user_id)
    if premium_record and premium_record.get('active'):
        expiry_date = premium_record.get('expiry_date')
        if expiry_date and expiry_date < datetime.now():
            # Premium Expired
            await db.update_premium_data(user_id, {"active": False})
            res["is_expired"] = True
        else:
            res["is_premium"] = True
            res["unlimited"] = True
            plan_name = premium_record.get('plan')
            plan = plans.get(plan_name, {})
            res["priority_queue"] = plan.get('priority_queue', False)
            res["daily_remaining"] = 999
            return res

    # 4. Free User
    daily_limit = config_dict.get('DAILY_TASK_LIMIT', 2) or 2
    user_stats = await db.get_user_stats(user_id)
    daily_used = user_stats.get('daily_used', 0) if user_stats else 0

    # Check for daily reset
    last_reset = user_stats.get('last_reset') if user_stats else None
    if last_reset and last_reset.date() < datetime.now().date():
        daily_used = 0
        await db.update_user_stats(user_id, {"daily_used": 0, "last_reset": datetime.now()})

    res["daily_remaining"] = max(0, daily_limit - daily_used)

    return res
