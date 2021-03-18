import json
import telebot
from bot.handlers_manager import Manager

__author__ = 'Обыденный И.В.'


class Bot:
    """Класс для работы с ботом"""
    def __init__(self):
        self.token = ''

        with open('config.json') as f:
            cfg = json.load(f)
            if 'token' in cfg:
                self.token = cfg['token']

        self.bot = telebot.TeleBot(self.token)

        self.handlers_manager = Manager(self.bot)
        self.handlers_manager.handle()

    def start(self):
        self.bot.polling(none_stop=True)
