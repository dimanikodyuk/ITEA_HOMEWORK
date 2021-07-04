import config
from telebot import TeleBot, types
from envparse import Env
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

DB_URL = "sqlite:///order_service_db.db"

my_apply = Flask("my_first_app")
my_apply.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(my_apply)

env = Env()
TOKEN = env.str("TOKEN")

bot = TeleBot(config.tg_token)


class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100))

class Employees(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(100), unique=True)
    position = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

class Applications(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    updated_dt = db.Column(db.DateTime)
    order_type = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    serial_no = db.Column(db.Integer, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    type = db.Column(db.String(100))
    comment = db.Column(db.Text)

class Telegram_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    nickname = db.Column(db.String(100))
    chat_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    message = db.Column(db.Text)
    type = db.Column(db.String(100))

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(100))
    created_dt = db.Column(db.DateTime)
    chat_id = db.Column(db.Integer)
    nickname = db.Column(db.String(100))
    role = db.Column(db.Integer)
    is_subscribed = db.Column(db.Integer)
    phone = db.Column(db.String(100))


# При авторизации у человека появится кнопка "Авторизация", при нажатии которой ему будет предложено поделиться номером телефона
def autorization(p_user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton('Авторизация', request_contact=True)])
    bot.send_message(p_user_id, """ Для продолжения нужна авторизация """, parse_mode="HTML", reply_markup=keyboard)

# Регистрация пользователя. Автоматически происходит подпись пользователя на рассылку новостей и прочего
def registration(p_chat_id, p_nickname, p_phone):
    dt = datetime.now()
    user_cr = Customers(fio = "New", created_dt = dt, chat_id = p_chat_id, nickname=p_nickname, role = 1, is_subscribed = 1, phone = p_phone)
    db.session.add(user_cr)
    db.session.flush()
    db.session.commit()


# Когда человек заходит в бот и пишет /start (нажимает кнопку), переходим к авторизации
@bot.message_handler(commands=['start'])
def start(m):
    autorization(m.chat.id)

# Проверка пользователя на наличие в БД по номеру телефону
def check_customer_phone(p_phone):
    # запрос в БД
    sql_dep = db.select(Customers.id).where(Customers.phone == f'{p_phone}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

def check_customer_nickname(nickname):
    # запрос в БД
    sql_dep = db.select(Customers.id).where(Customers.nickname == f'{nickname}')
    # выполнение запроса
    res = db.session.execute(sql_dep).fetchone()
    return res

# Меню которое отображается после авторизации/регистрации пользователем
def menu_user(p_user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton('Создать заявку')])
    keyboard.add(*[types.KeyboardButton('Созданные Вами заявки')])
    bot.send_message(p_user_id, """ Сделайте Ваш выбор: """, parse_mode="HTML", reply_markup=keyboard)

# Логика которая отрабатывает после передачи номера телефона пользователем
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
        if message.from_user.username is None:
            user = "Неизвестный"
        else:
            user = message.from_user.username
        phone = message.contact.phone_number
        res = check_customer_phone(phone)
        if res is None:
            registration(message.from_user.id, user, phone)
            bot.send_message(message.from_user.id, "Проводим регистрацию")

            # Обновление ФИО пользователя в БД
            msg = bot.reply_to(message, "Укажите Ваше ФИО:")
            bot.register_next_step_handler(msg, handle_check_fio)

        else:
            bot.send_message(message.from_user.id, "Авторизация прошла успешно. Добро пожаловать на наш сервис.")
            menu_user(message.from_user.id)

def handle_check_fio(message):
    fio = message.text
    res = check_customer_nickname(message.from_user.username)
    user = Customers.query.get(res[0])

    user.fio = fio
    db.session.commit()
    bot.send_message(message.from_user.id, f"Спасибо за регистрацию, {fio}. Добро пожаловать на наш сервис.")

    dt = datetime.now()
    telegram_log = Telegram_logs(created_dt = dt, nickname=fio, chat_id=message.from_user.id, customer_id=res[0], message="", type="Регистрация пользователя")
    db.session.add(telegram_log)
    db.session.flush()
    db.session.commit()

    menu_user(message.from_user.id)

# Меню типов заявки
def type_order(p_user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton('Проблема')])
    keyboard.add(*[types.KeyboardButton('Консультация')])
    bot.send_message(p_user_id, """ Сделайте Ваш выбор: """, parse_mode="HTML", reply_markup=keyboard)

# Регистрация проблемы
def reg_app_problem(message):
    res = check_customer_nickname(message.from_user.username)
    if res is None:
        bot.send_message(message.from_user.id, "Произошла ошибка, обратитесь к администратору.")
    else:
        msg_text = message.text
        bot.send_message(message.from_user.id, f"Мы зарегестрировали Вашу проблему: {msg_text}")

        dt = datetime.now()
        # creator_id - это ид пользователя, который создает заявку
        # executor_id = 1 это заявка автоматически падает на админа, потом будет распределение
        apply = Applications(created_dt=dt, order_type="Проблема", description=msg_text, status="New",
                             serial_no=str(uuid.uuid4()), creator_id=res[0], executor_id = 1)
        db.session.add(apply)
        db.session.flush()
        db.session.commit()

        dt = datetime.now()
        telegram_log = Telegram_logs(created_dt=dt, nickname=message.from_user.username, chat_id=message.from_user.id, customer_id=res[0],
                                     message=msg_text, type="Регистрация проблемы")
        db.session.add(telegram_log)
        db.session.flush()
        db.session.commit()

        menu_user(message.from_user.id)

# Регистрация запроса на консультацию
def reg_app_consult(message):

    res = check_customer_nickname(message.from_user.username)
    if res is None:
        bot.send_message(message.from_user.id, "Произошла ошибка, обратитесь к администратору.")
    else:
        msg_text = message.text
        bot.send_message(message.from_user.id, f"Мы зарегестрировали Ваш запрос на консультацию по вопросу: {msg_text}")

        dt = datetime.now()
        # creator_id - это ид пользователя, который создает заявку
        # executor_id = 1 это заявка автоматически падает на админа, потом будет распределение
        apply = Applications(created_dt=dt, order_type="Консультация", description=msg_text, status="New",
                             serial_no=str(uuid.uuid4()), creator_id=res[0], executor_id=1)
        db.session.add(apply)
        db.session.flush()
        db.session.commit()

        dt = datetime.now()
        telegram_log = Telegram_logs(created_dt=dt, nickname=message.from_user.username, chat_id=message.from_user.id,
                                     customer_id=res[0],
                                     message=msg_text, type="Регистрация заявки на консультацию")
        db.session.add(telegram_log)
        db.session.flush()
        db.session.commit()

        menu_user(message.from_user.id)


# Выбор типа проблемы
def reg_app(message):
    if message.text == "Проблема":
        msg = bot.reply_to(message, "Укажите суть проблемы:")
        bot.register_next_step_handler(msg, reg_app_problem)
    elif message.text == "Консультация":
        msg = bot.reply_to(message, "Укажите какая информация вас интересует:")
        bot.register_next_step_handler(msg, reg_app_consult)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    print(message.text)
    if message.text == "Создать заявку":
        print("Переходим к созданию заявки")

        msg = bot.reply_to(message, "Выберите тип заявки:")
        type_order(message.from_user.id)
        bot.register_next_step_handler(msg, reg_app)


    elif message.text == "Созданные Вами заявки":

            res = check_customer_nickname(message.from_user.username)
            sql = db.select(Applications.order_id, Applications.created_dt, Applications.status, Applications.executor_id).where(Applications.creator_id == f'{res[0]}')
            res = db.session.execute(sql).fetchall()
            for i in res:
                if i[3] == 1 or i[3] is None:
                    executor = 'Не назначен'
                else:
                    executor = i[3]
                res_text = f"""
<b>Номер заявки в системе:</b> {i[0]}
<b>Дата создания:</b> {i[1]}
<b>Статус:</b> {i[2]}
<b>Ответственный:</b> {executor}
                """
                bot.send_message(message.from_user.id, res_text, parse_mode="HTML")

    else:
        nick = message.from_user.username
        res = check_customer_nickname(nick)
        if res is None:
            res_text = f"Неизвестная команда: {message.text} от незарегестрированного пользователя: {message.from_user.username} с id: {message.from_user.id}"
            dt = datetime.now()

            telegram_log = Telegram_logs(created_dt=dt, nickname=nick, chat_id=message.from_user.id, customer_id=0,
                                         message=message.text, type="Получено сообщение")
            db.session.add(telegram_log)
            db.session.flush()
            db.session.commit()
        else:
            bot.send_message(message.from_user.id, "Неизвестная команда")
            dt = datetime.now()
            telegram_log = Telegram_logs(created_dt=dt, nickname=nick, chat_id=message.from_user.id, customer_id=res[0],
                                         message=message.text, type="Получено сообщение")
            db.session.add(telegram_log)
            db.session.flush()
            db.session.commit()


bot.polling()

# 310797108