from telebot import TeleBot
from telebot import types
from bot.task_template import TaskTemplate
from bot.message_sender import MessageSender

__author__ = 'Обыденный И.В.'


class CreateTaskHandler:
    """Класс содержит методы для создания задачи"""
    def __init__(self, bot: TeleBot, task_templates: dict):
        self.bot = bot
        self.task_templates = task_templates
        self.sender = MessageSender(bot)

    def create_task(self, msg: types.Message):
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

    def back(self, msg: types.Message):
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

    def next(self, msg: types.Message):
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

    def cancel(self, msg: types.Message):
        if msg.chat.id in self.task_templates:
            del self.task_templates[msg.chat.id]
        self.sender.main_menu(msg.chat.id)

    def to_execute(self, msg: types.Message):
        # TODO: Отправить на выполнение через API
        if msg.chat.id in self.task_templates:
            del self.task_templates[msg.chat.id]
        self.sender.execute(msg.chat.id)