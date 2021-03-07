"""Обработчик команды start"""
import telebot
from telebot import types

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    @bot.message_handler(commands=['start'])
    def start(msg):
        markup = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton('Start', callback_data='start callback')
        markup.add(item)
        bot.send_message(msg.chat.id, 'Вас приветствует mini-jira-bot!', reply_markup=markup)
