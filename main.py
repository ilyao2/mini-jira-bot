"""Телеграм-бот для работы с mini-jira API"""
import json
import telebot
from telebot import types

__author__ = 'Обыденный И.В.'


TOKEN = ''

with open('config.json') as f:
    cfg = json.load(f)
    if 'token' in cfg:
        TOKEN = cfg['token']

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton('Button 1', callback_data='Button 1 click')
    markup.add(item)
    bot.send_message(msg.chat.id, 'Вас приветствует mini-jira-bot!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(msg):
    markup = types.ReplyKeyboardMarkup()
    bot.send_message(msg.chat.id, msg.text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_button1(call):
    bot.send_message(call.message.chat.id, call.data)


bot.polling(none_stop=True)

