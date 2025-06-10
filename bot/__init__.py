

import json

from chatwoot import create_new_message


def process_pending_user_messages(payload):
    account_id=payload["account_id"]
    conversation_id=payload["conversation_id"]
    name=payload["name"]
    email=payload["email"]
    phonenumber=payload["phonenumber"]
    content=payload["content"]
    
    create_new_message(account_id, conversation_id, f"{name}: {content}")

