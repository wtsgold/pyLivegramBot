from connection import database_query, database_query_spec
import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

def text(message):
    try:
        get = database_query("SELECT user_id FROM blocked WHERE user_id = ?", (message.from_user.id,))
        print(get)
        if get != []:
            bot.send_message(message.chat.id, config.banned)
        else:
            if message.chat.id != config.main_id:
                # 检查消息是否是转发的
                if message.forward_from is None:
                    # 发送文本消息而不是转发
                    sent_message = bot.send_message(config.main_id, message.text)
                    database_query("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",
                                   (message.from_user.id, message.from_user.first_name, sent_message.message_id, message.text))
                    bot.send_message(message.chat.id, config.text_message)
                    print(message.message_id)
                else:
                    bot.send_message(message.chat.id, config.notallowed)
            elif message.chat.id == config.main_id:
                if message.reply_to_message is None:
                    # 发送文本消息而不是转发
                    sent_message = bot.send_message(config.main_id, message.text)
                    database_query("INSERT INTO USERS VALUES(?,?,?,?)",
                                   (message.from_user.id, message.from_user.first_name, sent_message.message_id, message.text))
                    bot.send_message(message.chat.id, config.text_message)
                elif message.reply_to_message is not None:
                    print(message.reply_to_message.message_id)
                    users = database_query("SELECT user_id FROM USERS WHERE messageid = ?", (message.reply_to_message.message_id,))
                    for i in users:
                        print(i[0])
                        bot.send_message(i[0], message.text)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, config.blocked)

# 您需要的其他处理器和逻辑
