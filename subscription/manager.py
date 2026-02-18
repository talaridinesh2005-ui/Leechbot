#!/usr/bin/env python3
from datetime import datetime, timedelta
from bot.helper.ext_utils.db_handler import DbManger
from subscription.plans import plans
from bot import OWNER_ID, bot, LOGGER

async def activate_premium(user_id, plan_name, transaction_id):
    plan = plans.get(plan_name)
    if not plan:
        LOGGER.error(f"Invalid plan name: {plan_name}")
        return False

    db = DbManger()
    duration_days = plan.get('duration_days', 30)
    start_date = datetime.now()
    expiry_date = start_date + timedelta(days=duration_days)

    premium_data = {
        "user_id": user_id,
        "plan": plan_name,
        "start_date": start_date,
        "expiry_date": expiry_date,
        "active": True,
        "transaction_id": transaction_id
    }

    await db.update_premium_data(user_id, premium_data)

    # Reset daily quota for new premium user
    await db.update_user_stats(user_id, {"daily_used": 0, "last_reset": datetime.now()})

    LOGGER.info(f"Premium activated for user {user_id}: Plan {plan_name}, Expiry {expiry_date}")

    # Send confirmation message
    try:
        msg = f"✅ Premium Activated Successfully\nPlan: {plan_name.capitalize()}\nExpiry: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}\nEnjoy Unlimited Access 🚀"
        await bot.send_message(user_id, msg)
    except Exception as e:
        LOGGER.error(f"Failed to send activation message to {user_id}: {e}")

    return True

async def check_expiries():
    db = DbManger()
    all_premium = await db.get_all_premium_data()
    now = datetime.now()
    for record in all_premium:
        user_id = record.get('user_id')
        if record.get('active') and record.get('expiry_date') < now:
            await db.update_premium_data(user_id, {"active": False})
            try:
                await bot.send_message(user_id, "⚠️ Your premium has expired.")
            except Exception as e:
                LOGGER.error(f"Failed to send expiry message to {user_id}: {e}")

        # Auto Cleanup: Remove expired records older than 90 days
        elif not record.get('active') and record.get('expiry_date') < now - timedelta(days=90):
            # We don't have a direct delete_premium in DbManger yet, let's just mark for deletion or leave it
            # Actually, I'll add delete_premium_data to DbManger
            await db.delete_premium_data(user_id)

async def cleanup_system():
    # Clear temp payment cache / transactions older than 24h
    # This is a placeholder for more complex cleanup
    LOGGER.info("Running System Cleanup...")
    # Log rotation is usually handled by the OS/container,
    # but we can truncate log.txt if it's too large
    try:
        if ospath.exists('log.txt') and ospath.getsize('log.txt') > 10 * 1024 * 1024: # 10MB
            with open('log.txt', 'w') as f:
                f.truncate(0)
            LOGGER.info("Log rotated.")
    except Exception as e:
        LOGGER.error(f"Cleanup Error: {e}")
