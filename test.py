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
    
    
