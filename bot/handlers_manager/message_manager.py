"""Модуль для управления обработчиками сообщений"""
import telebot
from bot.task_template import TaskTemplate
from bot.message_sender import MessageSender
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

    def handle(self):
        self.msg_dict[names.CREATE_TASK] = self._create_task
        self.msg_dict[names.TASKS_LIST] = self._tasks_list
        self.msg_dict[names.SHOW_WEB] = self._show_web
        self.msg_dict[names.BACK] = self._back
        self.msg_dict[names.CANCEL] = self._cancel
        self.msg_dict[names.NEXT] = self._next
        self.msg_dict[names.TO_EXECUTE] = self._to_execute

        @self.bot.message_handler(content_types=['text'])
        def base_message(msg: types.Message):
            self._base_message(msg)

    def _base_message(self, msg: types.Message):
        if msg.text in self.msg_dict:
            self.msg_dict[msg.text](msg)
        elif msg.chat.id in self.task_templates:
            self._create_task(msg)
        else:
            self.sender.unknowing_msg(msg.chat.id)

    def _create_task(self, msg: types.Message):
        # TODO: Избавиться от дублирования в _back и _next
        chat_id = msg.chat.id
        if chat_id in self.task_templates:
            task: TaskTemplate = self.task_templates[chat_id]

            if task.state == task.State.title_input:
                task.title = msg.text
                task.state = task.State.reporter_input
                self.sender.input_executor(chat_id, task)

            elif task.state == task.State.reporter_input:
                # TODO: load users id

                task.reporter_uuid = msg.text
                task.state = task.State.description_input
                self.sender.input_description(chat_id, task)

            elif task.state == task.State.description_input:
                task.description = msg.text
                task.state = task.State.deadline_input
                self.sender.input_deadline(chat_id, task)

            elif task.state == task.State.deadline_input:
                task.state = task.State.ready
                self.sender.to_execute(chat_id, task)
        else:
            self.task_templates[chat_id] = TaskTemplate()
            self.sender.input_title(chat_id)

    def _tasks_list(self, msg: types.Message):
        # TODO: задачи сортируются по дате
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заголовок задачи 1', callback_data='task: 1'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 2', callback_data='task: 2'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 3', callback_data='task: 3'))
        self.bot.send_message(msg.chat.id, names.TASKS_LIST, reply_markup=markup)

    def _show_web(self, msg: types.Message):
        self.bot.send_message(msg.chat.id, names.SHOW_WEB)

    def _back(self, msg: types.Message):
        if msg.chat.id in self.task_templates:
            task = self.task_templates[msg.chat.id]

            if task.state == task.State.reporter_input:
                task.state = task.State.title_input
                self.sender.input_title(msg.chat.id)

            elif task.state == task.State.description_input:
                task.state = task.State.reporter_input
                self.sender.input_executor(msg.chat.id, task)

            elif task.state == task.State.deadline_input:
                task.state = task.State.description_input
                self.sender.input_description(msg.chat.id, task)

            elif task.state == task.State.ready:
                task.state = task.State.deadline_input
                self.sender.input_deadline(msg.chat.id, task)

            else:
                del self.task_templates[msg.chat.id]
                self.sender.main_menu(msg.chat.id)
        else:
            self.sender.main_menu(msg.chat.id)

    def _next(self, msg: types.Message):
        if msg.chat.id in self.task_templates:
            task = self.task_templates[msg.chat.id]
            if task.state == task.State.description_input:
                task.state = task.State.deadline_input
                self.sender.input_deadline(msg.chat.id, task)

            elif task.state == task.State.deadline_input:
                task.state = task.State.ready
                self.sender.to_execute(msg.chat.id, task)

            else:
                del self.task_templates[msg.chat.id]
                self.sender.main_menu(msg.chat.id)
        else:
            self.sender.main_menu(msg.chat.id)

    def _cancel(self, msg: types.Message):
        if msg.chat.id in self.task_templates:
            del self.task_templates[msg.chat.id]
        self.sender.main_menu(msg.chat.id)

    def _to_execute(self, msg: types.Message):
        # TODO: Отправить на выполнение через API
        if msg.chat.id in self.task_templates:
            del self.task_templates[msg.chat.id]
        self.sender.execute(msg.chat.id)
