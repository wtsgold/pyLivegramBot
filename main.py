from flask import Flask, request
import telebot
import sqlite3

# 配置信息
TOKEN = "6933972200:AAFHM46cokafjAjwIbDwQE9kWiiZwzt8d3A"  # 请替换为您的 Telegram bot 的 Token
main_id = -4023133608  # 请替换为您的主要 ID
blocked_msg = "bot was blocked by the user"
start_msg = "Hello! This is your start message!"
ban_msg = "you were banned by the admin!"
unban_msg = "you were unbanned by the admin."
text_message = "Message that would be sent if somebody writes any text"
banned_msg = "you are blocked"

# 创建 Flask 应用
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# 数据库操作
def create_db_new():
    with sqlite3.connect('users.db', check_same_thread=False) as db:
        sql = db.cursor()
        sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
            user_id INTEGER,
            first_name VARCHAR,
            messageid INT,
            message VARCHAR)''')
        sql.execute('''CREATE TABLE IF NOT EXISTS blocked(
            user_id INT)''')
        sql.execute('''CREATE TABLE IF NOT EXISTS user(
            user_id INT)''')

def database_query(query, params=()):
    with sqlite3.connect('users.db', check_same_thread=False) as db:
        sql = db.cursor()
        sql.execute(query, params)
        db.commit()
        return sql.fetchall()

# 消息处理函数
def start(message):
    try:
        bot.send_message(message.chat.id, start_msg)
        info = database_query("SELECT user_id FROM user WHERE user_id = ?", (message.from_user.id,))
        if info == []:
            database_query("INSERT INTO user VALUES(?)", (message.from_user.id,))
    except Exception as e:
        print(str(e))

# 其他处理函数...

# 设置 webhook 路由
@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# 设置 bot 的处理函数
@bot.message_handler(commands=['start'])
def start_handler(message):
    start(message)

# 其他 bot.message_handler 装饰器

# 启动 Flask 应用
if __name__ == "__main__":
    create_db_new()  # 创建数据库（如果尚未创建）
    app.run(debug=True)
