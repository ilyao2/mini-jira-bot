"""Основной обработчик сообщений"""
import telebot
from telebot import types
from handlers_manager import names

__author__ = 'Обыденный И.В.'

msg_dict = {}


def handle(bot: telebot):
    @bot.message_handler(content_types=['text'])
    def answer(msg):
        if msg.text in msg_dict:
            msg_dict[msg.text](msg)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
            markup.add(types.KeyboardButton(names.CREATE_TASK), types.KeyboardButton(names.TASKS_LIST), row_width=2)
            markup.add(types.KeyboardButton(names.SHOW_WEB))
            bot.send_message(msg.chat.id, names.UNKNOWING_MESSAGE, reply_markup=markup)
