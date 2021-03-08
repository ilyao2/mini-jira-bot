"""Модуль для управления обработчиками колбэков"""
import telebot
from telebot import types

__author__ = 'Обыденный И.В.'


class CallbackManager:
    """Класс для управления обработчиками сообщений"""

    def __init__(self, bot: telebot.TeleBot):
        self.call_dict = {}
        self.bot = bot

    def handle(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call: types.CallbackQuery):
            self._base_callback(call)

    def _base_callback(self, call: types.CallbackQuery):
        self.bot.send_message(call.message.chat.id, call.data)
        # TODO: Обработчик, парсер call.data
