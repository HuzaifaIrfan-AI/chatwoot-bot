from bot import State
import json
import os
import logging

DEFAULT_SYSTEM_MESSAGE="""
You are an AI Chat Bot at Middlehost Webhosting Platform
"""


SYSTEM_MESSAGE = os.getenv("SYSTEM_MESSAGE", DEFAULT_SYSTEM_MESSAGE)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

import logging
generator_logger=logging.getLogger("generator")

# generator_logger.info(f"SYSTEM_MESSAGE: '''{SYSTEM_MESSAGE}'''")



generator_logger.info(f"Using OpenAI Model'{OPENAI_MODEL}'")
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.1,
    openai_api_key=OPENAI_API_KEY
)




def generate(state: State):
    generator_logger.info("---GENERATE---")

    user_content = state["user_content"]
    state_messages = state["messages"]
    documents = state["documents"]
    
    # generator_logger.info(f"'''{documents}\n\n'''")
    
    generator_logger.info(f"user_content: {user_content}")


    messages = [
        {"role": "system",
         "content": SYSTEM_MESSAGE
         }
    ]
    
    for message in state_messages:
        messages.append(message)

    context_message = {
        "role": "user",
        "content": f"""{documents}

Question:
{user_content}"""
    }

    messages.append(context_message)

    generation = llm.invoke(messages)


    try:
        bot_content = generation.content
    except:
        bot_content = generation

    generator_logger.info(f"bot_content: {bot_content}")
    
    return {"bot_content": bot_content}