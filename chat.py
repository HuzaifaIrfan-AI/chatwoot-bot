
# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)


import config

import logger_config

from bot import process_pending_user_messages

def main():
        
    while(1):
        user_content=input("\nUser: ")

        payload = {
            "account_id": 1,
            "conversation_id": 1,
            "name": "User",
            "email": None,
            "phonenumber": None,
            "content": user_content
        }
        
        bot_content=process_pending_user_messages(payload)
        
        print(f"Bot: {bot_content}")
        
        
            

if __name__ == "__main__":
    main()