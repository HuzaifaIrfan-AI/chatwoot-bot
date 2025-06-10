
import logging
import time
# Configure logging
chatwoot_logger=logging.getLogger("chatwoot")
chatwoot_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/chatwoot.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
chatwoot_logger.addHandler(handler)

pending_user_messages_logger=logging.getLogger("pending_user_messages")
pending_user_messages_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/pending_user_messages.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
pending_user_messages_logger.addHandler(handler)


bot_logger=logging.getLogger("bot")
bot_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/bot.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
bot_logger.addHandler(handler)

retriever_logger=logging.getLogger("retriever")
retriever_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/retriever.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
retriever_logger.addHandler(handler)


generator_logger=logging.getLogger("generator")
generator_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/generator.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
generator_logger.addHandler(handler)