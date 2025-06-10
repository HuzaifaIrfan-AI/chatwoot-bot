
import os
KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9092")
print(f"KAFKA_URL at '{KAFKA_URL}'")

from confluent_kafka import Producer, Consumer, KafkaException

import json

producer = Producer({'bootstrap.servers': KAFKA_URL})

def create_new_message(account_id,conversation_id,content):
    
    payload={
        "account_id":account_id,
        "conversation_id":conversation_id,
        "content":content
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


def open_conversation_status(account_id,conversation_id):
    
    payload={
        "account_id":account_id,
        "conversation_id":conversation_id
    }
    # Serialize to JSON and send
    producer.produce(
        topic='open_conversation_status',
        key=str(payload["conversation_id"]),
        value=json.dumps(payload).encode('utf-8'),
        callback=lambda err, msg, val=payload: (
            print(f"❌ Failed to deliver: {err}") if err else print(
                f"✅ {msg.topic()} Delivered: {val}")
        )
    )
    producer.flush()
    