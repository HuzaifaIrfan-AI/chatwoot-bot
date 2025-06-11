
# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)


import config

import logger_config

from bot.State import State, default_state

from bot import bot

def main():
        
    while(1):
        user_content=input("\nUser: ")

        state = default_state()
        state["conversation_id"] = str(1)
        state["user_content"] = user_content
        state = bot.invoke(state)
        bot_content=state["bot_content"]

        print(f"Bot: {bot_content}")
        
            

if __name__ == "__main__":
    main()