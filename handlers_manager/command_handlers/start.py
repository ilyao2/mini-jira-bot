"""Обработчик команды start"""
import telebot
from telebot import types
from handlers_manager import names

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(msg):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        markup.add(types.KeyboardButton(names.CREATE_TASK), types.KeyboardButton(names.TASKS_LIST), row_width=2)
        markup.add(types.KeyboardButton(names.SHOW_WEB))
        bot.send_message(msg.chat.id, names.HELLO, reply_markup=markup)
