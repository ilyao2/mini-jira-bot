"""Модуль для управления обработчиками команд  (Для обработки инлайн кнопок)"""
import telebot
from telebot import types
from bot.handlers_manager import names

__author__ = 'Обыденный И.В.'


class CommandManager:
    """Класс для управления обработчиками команд"""

    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def handle(self):
        @self.bot.message_handler(commands=['auth'])
        def auth(msg: types.Message):
            self._auth_handler(msg)

        @self.bot.message_handler(commands=['start'])
        def start(msg: types.Message):
            self._start_handler(msg)

    def _auth_handler(self, msg: types.Message):
        # TODO: auth command
        markup = types.InlineKeyboardMarkup()
        item = types.InlineKeyboardButton('Auth', callback_data='auth callback')
        markup.add(item)
        self.bot.send_message(msg.chat.id, 'Вас приветствует mini-jira-bot!', reply_markup=markup)

    def _start_handler(self, msg: types.Message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        markup.add(types.KeyboardButton(names.CREATE_TASK), types.KeyboardButton(names.TASKS_LIST), row_width=2)
        markup.add(types.KeyboardButton(names.SHOW_WEB))
        self.bot.send_message(msg.chat.id, names.HELLO, reply_markup=markup)
