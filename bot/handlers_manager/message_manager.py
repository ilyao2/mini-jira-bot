"""Модуль для управления обработчиками сообщений"""
import telebot
import json
import requests
from bot.message_sender import MessageSender
from bot.handlers_manager.handlers.create_task_handler import CreateTaskHandler
from telebot import types
from bot.handlers_manager import names

__author__ = 'Обыденный И.В.'


class MessageManager:
    """Класс для управления обработчиками сообщений"""

    def __init__(self, bot: telebot.TeleBot):
        self.msg_dict = {}
        self.task_templates = {}
        self.bot = bot
        self.sender = MessageSender(bot)
        self.create_task_handler = CreateTaskHandler(self.bot, self.task_templates)

    def handle(self):
        self.msg_dict[names.CREATE_TASK] = self.create_task_handler.create_task
        self.msg_dict[names.TASKS_LIST] = self._tasks_list
        self.msg_dict[names.SHOW_WEB] = self._show_web
        self.msg_dict[names.BACK] = self.create_task_handler.back
        self.msg_dict[names.CANCEL] = self.create_task_handler.cancel
        self.msg_dict[names.NEXT] = self.create_task_handler.next
        self.msg_dict[names.TO_EXECUTE] = self.create_task_handler.to_execute

        @self.bot.message_handler(content_types=['text'])
        def base_message(msg: types.Message):
            self._base_message(msg)

    def _base_message(self, msg: types.Message):
        if msg.text in self.msg_dict:
            self.msg_dict[msg.text](msg)
        elif msg.chat.id in self.task_templates:
            self.create_task_handler.create_task(msg)
        else:
            self.sender.unknowing_msg(msg.chat.id)

    def _tasks_list(self, msg: types.Message):
        response = requests.get(names.BASE_URL+'tg/view/'+str(msg.chat.id))
        tasks = response.json()

        # TODO: задачи сортируются по дате
        # TODO: проверка на исполнение запроса

        markup1 = types.InlineKeyboardMarkup()
        for task in tasks['reporter']:
            data = 'show_task/{}'.format(task['id'])
            markup1.add(types.InlineKeyboardButton(task['title'], callback_data=data))

        markup2 = types.InlineKeyboardMarkup()
        for task in tasks['executor']:
            data = 'show_task/{}'.format(task['id'])
            markup2.add(types.InlineKeyboardButton(task['title'], callback_data=data))

        self.bot.send_message(msg.chat.id, 'Задачи, где вы постановщик:', reply_markup=markup1)
        self.bot.send_message(msg.chat.id, 'Задачи, где вы исполнитель:', reply_markup=markup2)

    def _show_web(self, msg: types.Message):
        self.bot.send_message(msg.chat.id, names.SHOW_WEB)
