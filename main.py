"""Телеграм-бот для работы с mini-jira API"""
import json
import telebot
import handlers_manager

__author__ = 'Обыденный И.В.'

TOKEN = ''

with open('config.json') as f:
    cfg = json.load(f)
    if 'token' in cfg:
        TOKEN = cfg['token']

bot = telebot.TeleBot(TOKEN)
handlers_manager.handle(bot)
bot.polling(none_stop=True)
