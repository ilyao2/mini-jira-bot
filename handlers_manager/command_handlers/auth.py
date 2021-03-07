"""Обработчик команды auth"""
import telebot
from telebot import types

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    @bot.message_handler(commands=['auth'])
    def start(msg):
        # TODO: auth command
        markup = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton('Auth', callback_data='auth callback')
        markup.add(item)
        bot.send_message(msg.chat.id, 'Вас приветствует mini-jira-bot!', reply_markup=markup)
