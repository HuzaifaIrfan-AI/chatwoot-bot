# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)


import config

import logger_config


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


from bot import bot


def main():
    
    conversation_id="1"
    
    config = {"configurable": {"thread_id": conversation_id}}
        
    while(1):
        user_content=input("\nUser: ")

        inputs = {"open_conversation_state": False, "conversation_id":conversation_id, "messages": [HumanMessage(user_content)]}

        final_state = bot.invoke(inputs, config=config)
        
        bot_content = final_state["messages"][-1].content
        print(f"\nBot: {bot_content}")
        
        # print(final_state)
        # print("Final Chat State:\n")
        # for msg in final_state["messages"]:
        #     msg.pretty_print()
        
            

if __name__ == "__main__":
    main()