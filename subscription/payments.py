#!/usr/bin/env python3
from subscription.plans import plans
from bot.helper.telegram_helper.button_build import ButtonMaker

def get_payment_message(plan_name):
    plan = plans.get(plan_name)
    if not plan:
        return "Invalid Plan", None

    text = f"💎 <b>Premium Plan: {plan_name.capitalize()}</b>\n\n"
    text += f"💰 Price: ₹{plan['price']}\n"
    text += f"⏳ Duration: {plan['duration_days']} days\n"
    text += f"🚀 Leech: {plan['leech_limit']}\n"
    text += f"📂 Mirror: {plan['mirror_limit']}\n"
    text += f"⚡ Priority Queue: {'Yes' if plan['priority_queue'] else 'No'}\n\n"
    text += "💳 <b>Payment via UPI:</b>\n"
    text += "<code>yourupi@handle</code> (Example)\n\n"
    text += "📸 <b>Scan QR Code (If available) or Pay to UPI ID above.</b>\n\n"
    text += "📝 <b>After payment, send your 12-digit UTR number here.</b>"

    buttons = ButtonMaker()
    buttons.ibutton("Cancel", "premium cancel")

    return text, buttons.build_menu(1)
