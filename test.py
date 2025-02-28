import telebot
import configparser
import logging

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        # 加载配置
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # 创建机器人实例
        bot = telebot.TeleBot(config['TELEGRAM']['ACCESS_TOKEN'])

        # 定义消息处理器
        @bot.message_handler(func=lambda message: True)
        def echo(message):
            try:
                bot.reply_to(message, message.text.upper())
            except Exception as e:
                logger.error(f"Error in echo handler: {str(e)}")

        # 启动机器人
        logger.info("Starting bot...")
        bot.polling()

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
# import telegram
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, Updater
# #The message Handler is used for all message updates
# import configparser
# import logging

# def main():
#     # Load your token and create an Updater for your Bot
#     config =configparser.ConfigParser()
#     config.read('config.ini')
#     updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']),use_context=True)
#     dispatcher =updater.dispatcher
#     #You can set this logging module,
#     # so you will know when and why things do not work as expectedlogging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s -%(message)s',
#     logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s -%(message)s',level=logging.INFO)
#     #register adispatcher to handle message:
#     # here we register an echo dispatcher
#     echo_handler=MessageHandler(filters.text &(~filters.command),echo)
#     dispatcher.add_handler(echo_handler)
#     # To start the bot:
#     updater.start_polling()
#     updater.idle()
    
# def echo(update,context):
#     reply_message =update.message.text.upper()
#     logging.info("Update:"+ str(update))
#     logging.info("context:"+str(context))
#     context .bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    
# if __name__=="__main__":
#     main()
    
    
# """Basic connection example.
# """

# import redis

# r = redis.Redis(
#     host='redis-11571.crce178.ap-east-1-1.ec2.redns.redis-cloud.com',
#     port=11571,
#     decode_responses=True,
#     username="default",
#     password="JQJua0ZU9iDsICQwxbgrZB4cTCYl9jhB",
# )

# success = r.set('foo', 'bar')
# # True

# result = r.get('foo')
# print(result)
# >>> bar

