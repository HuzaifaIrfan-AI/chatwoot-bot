
import os
KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9092")
print(f"KAFKA_URL at '{KAFKA_URL}'")

from confluent_kafka import Producer, Consumer, KafkaException

producer = Producer({'bootstrap.servers': KAFKA_URL})

import json
import logging

def process_pending_user_messages(payload):
    account_id=payload["account_id"]
    conversation_id=payload["conversation_id"]
    name=payload["name"]
    email=payload["email"]
    phonenumber=payload["phonenumber"]
    content=payload["content"]
    
    

    payload={
        "account_id":account_id,
        "conversation_id":conversation_id,
        "content":f"{name}: {content}"
    }
    # Serialize to JSON and send
    producer.produce(
        topic='create_new_message',
        key=str(payload["conversation_id"]),
        value=json.dumps(payload).encode('utf-8'),
        callback=lambda err, msg, val=payload: (
            print(f"❌ Failed to deliver: {err}") if err else print(
                f"✅ {msg.topic()} Delivered: {val}")
        )
    )
    producer.flush()
    
    logging.info(json.dumps(payload))
    