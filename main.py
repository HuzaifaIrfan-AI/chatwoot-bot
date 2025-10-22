

import json
from confluent_kafka import Producer, Consumer, KafkaException
import os
import datetime


import config

from logger import pending_user_messages_logger

UTC_TIME_NOW = str(datetime.datetime.now(tz=datetime.UTC))

from settings import settings
KAFKA_URL = settings.KAFKA_URL

conf = {
    'bootstrap.servers': KAFKA_URL,
    'group.id': 'pending_user_messages_group',
    'auto.offset.reset': 'earliest'
}



pending_user_messages_logger.warning("pending_user_messages_consumer Started")


from bot import bot
from chatwoot import open_conversation_status, create_new_message
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


CONVERSATION_OPENED_CONTENT="Your chat is transferred to human. Please wait."

def process_pending_user_messages(payload):
    account_id=payload["account_id"]
    conversation_id=payload["conversation_id"]
    name=payload["name"]
    email=payload["email"]
    phonenumber=payload["phonenumber"]
    user_content=payload["content"]
    

    config = {"configurable": {"thread_id": conversation_id}}
    inputs = {"open_conversation_state": False, "conversation_id":conversation_id, "messages": [HumanMessage(user_content)]}

    final_state = bot.invoke(inputs, config=config)

    
    bot_content = final_state["messages"][-1].content

    open_conversation_state=final_state["open_conversation_state"]
    
    if (open_conversation_state):
        open_conversation_status(account_id, conversation_id)
        bot_content=CONVERSATION_OPENED_CONTENT
    
    create_new_message(account_id, conversation_id, bot_content)
    
    return bot_content




def test_consumer():
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


def main():

    # test_consumer()

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

            try:
                key = msg.key().decode('utf-8') if msg.key() else None
                value = msg.value().decode('utf-8') if msg.value() else None
                print(f"\nkey={key}, value={value}")
                payload = json.loads(value)
            except Exception as e:
                pending_user_messages_logger.error(f"[{key}] Error loading message: {str(e)}")
                continue
                

            try:
                pending_user_messages_logger.info(
                    f"[{payload["conversation_id"]}] "+json.dumps(payload))
                bot_content = process_pending_user_messages(payload)
                pending_user_messages_logger.info(
                    f"[{payload["conversation_id"]}] "+json.dumps(bot_content))
            except Exception as e:
                pending_user_messages_logger.error(
                    f"[{key}] Error processing message: {str(e)}")
                continue
                
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
