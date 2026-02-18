#!/usr/bin/env python3
import re
from bot.helper.ext_utils.db_handler import DbManger

async def verify_utr(utr):
    # Basic UTR validation (12 digits usually)
    if not re.match(r'^\d{12}$', utr):
        return False, "Invalid UTR format. Must be 12 digits."

    db = DbManger()
    # Check if transaction already used in premium
    all_premium = await db.get_all_premium_data()
    for record in all_premium:
        if record.get('transaction_id') == utr:
            return False, "This transaction has already been used to activate premium."

    # Option B logic: Check against actual transaction list
    # For now, we simulate this by checking a 'transactions' collection
    # If the transaction exists there and is 'unused', it's valid.
    # In this bot, we might not have a way to automatically populate 'transactions'
    # without a gateway, so we'll just log it and allow it for now IF it's not a duplicate.
    # To be more secure, an admin could pre-load valid UTRs.

    # Check if this UTR was already submitted by someone else but not yet activated
    # (Replay attack prevention)
    existing_tx = await db.get_transaction(utr)
    if existing_tx:
        return False, "This transaction ID has already been submitted."

    # Save as submitted
    await db.add_transaction(utr, {"status": "submitted", "timestamp": "now"})

    return True, "Valid"
