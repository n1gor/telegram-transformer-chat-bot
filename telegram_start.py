import logging
import os
import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from time import sleep

os.chdir(os.path.dirname(__file__))

from configs.config import DevConfig
from db_models.models import Base, User
from config_reader import read_config

from bots.chatbot import ChatBot

chatBot = ChatBot()
config_data = read_config()
API_TOKEN = DevConfig.TELEGRAM_TOKEN
bot = telebot.AsyncTeleBot(API_TOKEN)
engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

send_contact = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
hideBoard = telebot.types.ReplyKeyboardRemove()


def auth_decorator(func):
    @wraps(func)
    def auth_check(message):
        cid = message.chat.id
        if session.query(User).filter_by(telegram_id=cid).first():
            return func(message)
        else:
            send_contact.add(
                telebot.types.KeyboardButton("Send my phone number", request_contact=True))
            bot.send_message(cid, "I don't know you. Send you phone number to proceed",
                             reply_markup=send_contact)
            bot.register_next_step_handler(message, process_auth_check, func, message)

    return auth_check


def process_auth_check(message, func, msg):
    cid = message.chat.id
    phn = message.contact.phone_number
    if not message.contact:
        bot.send_message(cid, 'Please, push the button to send me your phone number')
    elif cid == message.contact.user_id:
        user = session.query(User).filter_by(phone_number=phn).first()
        if user:
            user.telegram_id = cid
            session.add(user)
            session.commit()
            bot.send_message(cid, 'You are registered now!', reply_markup=hideBoard)
            sleep(0.1)
            return func(msg)
        else:
            bot.send_message(cid, 'Access denied!')
    else:
        bot.send_message(cid, 'Wrong phone number!')


@bot.message_handler(commands=['start'])
@auth_decorator
def start_message(message):
    cid = message.chat.id
    bot.send_message(cid, f'Hello and welcome! Type something and we will start a conversation!')


@bot.message_handler(content_types=['text'])
@auth_decorator
def message_handler(message):
    bot.send_message(message.chat.id, chatBot.predict(message.text))


bot.polling(none_stop=True)
