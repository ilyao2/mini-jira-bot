"""Класс длля генерирования ответных сообщений"""
from telebot import TeleBot
from telebot import types
from bot.task_template import TaskTemplate
import requests
from bot.handlers_manager import names

__author__ = 'Обыденный И.В.'


class MessageSender:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.markups = {}
        self.__create_markups()

    def unknowing_msg(self, chat_id: types.Message):
        self.bot.send_message(chat_id, names.UNKNOWING_MESSAGE, reply_markup=self.markups['general'])

    def main_menu(self, chat_id: types.Message):
        self.bot.send_message(chat_id, names.MAIN_MENU, reply_markup=self.markups['general'])

    def execute(self, chat_id: types.Message):
        self.bot.send_message(chat_id, names.TO_EXECUTE, reply_markup=self.markups['general'])

    def input_title(self, chat_id: types.Message):
        self.bot.send_message(chat_id,
                              'Введите заголовок новой задачи.',
                              reply_markup=self.markups['in_creation'])

    def input_executor(self, chat_id: types.Message, task: TaskTemplate):
        text = 'Заголовок: {}\n\nВыберите исполнителя.'.format(task.title)
        self.bot.send_message(chat_id,
                              text,
                              reply_markup=self.markups['in_creation'])

    def input_description(self, chat_id: types.Message, task: TaskTemplate):
        text = 'Заголовок: {}\nИсполнитель: {}\n\nВведите описание задачи или нажмите "Далее".'
        text = text.format(task.title, task.reporter_uuid)
        self.bot.send_message(chat_id,
                              text,
                              reply_markup=self.markups['next'])

    def input_deadline(self, chat_id: types.Message, task: TaskTemplate):
        text = 'Заголовок: {}\n'
        text += 'Исполнитель: {}\n'
        text += 'Описание:\n{}\n\n'
        text += 'Введите срок выполнения задачи или нажмите "Далее".'
        text = text.format(task.title, task.reporter_uuid, task.description)
        self.bot.send_message(chat_id, text, reply_markup=self.markups['next'])

    def to_execute(self, chat_id: types.Message, task: TaskTemplate):
        text = 'Заголовок: {}\n'
        text += 'Исполнитель: {}\n'
        text += 'Описание:\n{}\n'
        text += 'Срок выполнения: {}\n\n'
        text += 'Проверьте правильность введённых данных и отправьте на исполнение.'
        text = text.format(task.title, task.reporter_uuid, task.description, str(task.deadline))
        self.bot.send_message(chat_id, text, reply_markup=self.markups['ready'])

    def __create_markups(self):
        self.markups['general'] = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        self.markups['general'].add(types.KeyboardButton(names.CREATE_TASK),
                                    types.KeyboardButton(names.TASKS_LIST),
                                    row_width=2)
        self.markups['general'].add(types.KeyboardButton(names.SHOW_WEB))

        self.markups['in_creation'] = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        self.markups['in_creation'].add(types.KeyboardButton(names.BACK),
                                        types.KeyboardButton(names.CANCEL),
                                        row_width=2)

        self.markups['ready'] = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        self.markups['ready'].add(types.KeyboardButton(names.BACK),
                                  types.KeyboardButton(names.CANCEL),
                                  row_width=2)
        self.markups['ready'].add(types.KeyboardButton(names.TO_EXECUTE))

        self.markups['next'] = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
        self.markups['next'].add(types.KeyboardButton(names.BACK),
                                 types.KeyboardButton(names.CANCEL),
                                 row_width=2)
        self.markups['next'].add(types.KeyboardButton(names.NEXT))
