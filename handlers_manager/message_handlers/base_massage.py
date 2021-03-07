"""Основной обработчик сообщений"""
import telebot
from telebot import types

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    @bot.message_handler(content_types=['text'])
    def answer(msg):
        markup = types.ReplyKeyboardMarkup()
        bot.send_message(msg.chat.id, msg.text, reply_markup=markup)
