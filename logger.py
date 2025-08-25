
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

retrieval_logger=logging.getLogger("retrieval")
retrieval_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/retrieval.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
retrieval_logger.addHandler(handler)


generation_logger=logging.getLogger("generation")
generation_logger.setLevel(logging.INFO)  # Or DEBUG if needed
handler=logging.FileHandler('log/generation.log',mode="a")
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s]  %(message)s'))
handler.formatter.converter=time.gmtime
generation_logger.addHandler(handler)