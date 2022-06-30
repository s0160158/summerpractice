import telebot
from telebot import types
import mysql.connector
import datetime

bot = telebot.TeleBot("5589052644:AAFuneGDDsZsWG-jCr48WEcOcNbFy7ybOrs")

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="project"
)

cursor = db.cursor()
now = datetime.datetime.now()

#cursor.execute("CREATE DATABASE project")

#cursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255))")

# for x in cursor:
   # print(x)

#cursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")

#sql = "INSERT INTO users (first_name, last_name, user_id) VALUES (%s, %s, %s)"
#val = ("Anton", "Dav","1")
#cursor.execute(sql, val)
#db.commit()

# print(cursor.rowcount, "Запись добавлена")

user_data = {}

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        msg = bot.send_message(message.chat.id, "Ваше имя")
        bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)

        msg = bot.send_message(message.chat.id, "Ваша фамилия")
        bot.register_next_step_handler(msg, process_lastname_step)
    except Exception as e:
        bot.reply_to(message, 'формальность')

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.last_name = message.text


        

        sql = "INSERT INTO users (first_name, last_name, user_id) \
                                  VALUES (%s, %s, %s)"
        val = (user.first_name, user.last_name, user_id)
        cursor.execute(sql, val)
        db.commit()

        bot.send_message(message.chat.id, "Вы успешно зарегистрированы")
    except Exception as e:
        bot.reply_to(message, 'Вы уже зарегистрированы')


        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Николай Второй')
        itembtn2 = types.KeyboardButton('Екатерина Вторая')
        itembtn3 = types.KeyboardButton('Александр Третий')
        itembtn4 = types.KeyboardButton('Владимир Ленин')
        itembtn5 = types.KeyboardButton('Владимир Путин')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        msg = bot.send_message(message.chat.id, "Кто правил Россией в 1901 году?", reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Николай Второй":
        bot.send_message(message.chat.id,"Да, молодец")
        
    if message.text=="Екатерина Вторая":
        bot.send_message(message.chat.id,"Нет, учи историю")
    
    if message.text=="Александр Третий":
        bot.send_message(message.chat.id,"Нет, учи историю")

    if message.text=="Владимир Ленин":
        bot.send_message(message.chat.id,"Нет, учи историю")

    if message.text=="Владимир Путин":
        bot.send_message(message.chat.id,"Ты шутишь?")


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

if __name__ == '__main__':
   bot.polling(none_stop=True)

