# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)

import datetime
UTC_TIME_NOW = str(datetime.datetime.now(tz=datetime.UTC))

import os
KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9092")
print(f"KAFKA_URL at '{KAFKA_URL}'")

from confluent_kafka import Producer, Consumer, KafkaException

conf = {
    'bootstrap.servers': KAFKA_URL,
    'group.id': 'pending_user_messages_group',
    'auto.offset.reset': 'earliest'
}

import json

import logging
import time

# Configure logging
logging.basicConfig(
    filename='log/pending_user_messages.log',
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'
)
logging.Formatter.converter = time.gmtime
logging.warning("pending_user_messages_consumer Started")


from bot import process_pending_user_messages

def main():
    producer = Producer({'bootstrap.servers': KAFKA_URL})
    
    payload = {
        "account_id": 1,
        "conversation_id": 1,
        "name": "AI Bot Test",
        "email": None,
        "phonenumber": None,
        "content": f"pending_user_messages test {UTC_TIME_NOW}"
    }
    
    # Serialize to JSON and send
    producer.produce(
        topic='pending_user_messages',
        key=str(payload["conversation_id"]),
        value=json.dumps(payload).encode('utf-8'),
        callback=lambda err, msg, val=payload: (
            print(f"❌ Failed to deliver: {err}") if err else print(
                f"✅ {msg.topic()} Delivered: {val}")
        )
    )
    producer.flush()
    
    
    consumer = Consumer(conf)
    consumer.subscribe(['pending_user_messages'])

    try:
        print("Listening for messages on 'pending_user_messages'... Press Ctrl+C to exit.")
        while True:
            msg = consumer.poll(0.1)  # Wait 1 second for a message

            if msg is None:
                continue  # No message this time
            if msg.error():
                raise KafkaException(msg.error())

            key = msg.key().decode('utf-8') if msg.key() else None
            value = msg.value().decode('utf-8') if msg.value() else None
            print(f"Received message: key={key}, value={value}")
            payload=json.loads(value)
            

            ret=process_pending_user_messages(payload)



    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        consumer.close()



if __name__ == "__main__":
    main()
