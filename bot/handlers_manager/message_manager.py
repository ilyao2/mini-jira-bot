"""Класс для управления обработчиками команд"""
import telebot
from telebot import types
from bot.handlers_manager import names

__author__ = 'Обыденный И.В.'


class MessageManager:
    """Класс для управления обработчиками сообщений"""

    def __init__(self, bot: telebot.TeleBot):
        self.msg_dict = {}
        self.bot = bot

    def handle(self):
        self.msg_dict[names.CREATE_TASK] = self._create_task
        self.msg_dict[names.TASKS_LIST] = self._tasks_list
        self.msg_dict[names.SHOW_WEB] = self._show_web

        @self.bot.message_handler(content_types=['text'])
        def base_message(msg: types.Message):
            self._base_message(msg)

    def _base_message(self, msg: types.Message):
        if msg.text in self.msg_dict:
            self.msg_dict[msg.text](msg)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
            markup.add(types.KeyboardButton(names.CREATE_TASK), types.KeyboardButton(names.TASKS_LIST), row_width=2)
            markup.add(types.KeyboardButton(names.SHOW_WEB))
            self.bot.send_message(msg.chat.id, names.UNKNOWING_MESSAGE, reply_markup=markup)

    def _create_task(self, msg: types.Message):
        self.bot.send_message(msg.chat.id, names.CREATE_TASK)

    def _tasks_list(self, msg: types.Message):
        # TODO: задачи сортируются по дате
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заголовок задачи 1', callback_data='task: 1'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 2', callback_data='task: 2'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 3', callback_data='task: 3'))
        self.bot.send_message(msg.chat.id, names.TASKS_LIST, reply_markup=markup)

    def _show_web(self, msg: types.Message):
        self.bot.send_message(msg.chat.id, names.SHOW_WEB)
