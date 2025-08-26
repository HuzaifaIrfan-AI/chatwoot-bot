
from settings import settings
QDRANT_URL = settings.QDRANT_URL
KAFKA_URL = settings.KAFKA_URL


from confluent_kafka import Producer, Consumer, KafkaException

import json

producer = Producer({'bootstrap.servers': KAFKA_URL})

from logger import chatwoot_logger

chatwoot_logger.warning("Chatwoot Producers Started")



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
            chatwoot_logger.error(f"❌ Failed to deliver: {err}") if err else chatwoot_logger.info(
                f"[{val["conversation_id"]}] ✅ {msg.topic()} {val}")
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
            chatwoot_logger.error(f"❌ Failed to deliver: {err}") if err else chatwoot_logger.info(
                f"[{val["conversation_id"]}] ✅ {msg.topic()} {val}")
        )
    )
    producer.flush()
    