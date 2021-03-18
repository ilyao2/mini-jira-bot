"""Модуль для управления обработчиками колбэков"""
import requests
import json
import telebot
from bot.handlers_manager import names
from telebot import types

__author__ = 'Обыденный И.В.'


class CallbackManager:
    """Класс для управления обработчиками сообщений"""

    def __init__(self, bot: telebot.TeleBot):
        self.call_dict = {}
        self.bot = bot

    def handle(self):
        self.call_dict['show_task'] = self._show_task_callback
        self.call_dict['change_status'] = self._change_status_callback

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call: types.CallbackQuery):
            self._base_callback(call)

    def _base_callback(self, call: types.CallbackQuery):
        call_data = call.data.partition('/')
        if call_data[2] != '' and call_data[0] in self.call_dict:
            callback_type = call_data[0]
            data = call_data[2]
            if callback_type in self.call_dict:
                self.call_dict[callback_type](call, data)
        else:
            self.bot.send_message(call.message.chat.id, 'Кнопка не работает ;(')

    def _show_task_callback(self, call: types.CallbackQuery, task_id: str):
        chat_id = call.message.chat.id
        # TODO: проверка запроса
        try:
            response = requests.get(names.BASE_URL+'tg/task/{}/{}'.format(task_id, chat_id))
            if response.status_code != 200:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            self.bot.answer_callback_query(call.id, 'Невозможно выполнить операцию', False)

        task = response.json()
        answer = task['title'] + '\n\n'
        if 'description' in task:
            answer += task['description']+'\n\n'

        if 'reporter' in task:
            answer += 'Автор задачи: {} {}\n'.format(task['reporter']['name'], task['reporter']['lastName'])

        if 'executor' in task:
            answer += 'Исполнитель: {} {}\n'.format(task['executor']['name'], task['executor']['lastName'])

        if 'deadline' in task:
            answer += 'deadline: ' + task['deadline']

        markup = types.InlineKeyboardMarkup()
        if 'state' in task:
            buttons = []
            if 'isExecutor' in task and task['isExecutor']:
                if task['state'] == 'CREATED':
                    data = 'change_status/{}/{}'.format(task_id, 'IN_PROGRESS')
                    buttons.append(types.InlineKeyboardButton('Взять в работу', callback_data=data))

                if task['state'] == 'IN_PROGRESS':
                    data = 'change_status/{}/{}'.format(task_id, 'WAITING')
                    buttons.append(types.InlineKeyboardButton('Отправить на подтверждение', callback_data=data))

            if 'isReporter' in task and task['isReporter']:
                if task['state'] == 'WAITING_APPROVED':
                    data = 'change_status/{}/{}'.format(task_id, 'CLOSED')
                    buttons.append(types.InlineKeyboardButton('Подтвердить', callback_data=data))
                    data = 'change_status/{}/{}'.format(task_id, 'IN_PROGRESS')
                    buttons.append(types.InlineKeyboardButton('Отправить на доработку', callback_data=data))

                if task['state'] in ['IN_PROGRESS', 'CREATED']:
                    data = 'change_status/{}/{}'.format(task_id, 'DELETED')
                    buttons.append(types.InlineKeyboardButton('Удалить', callback_data=data))

            if buttons:
                markup.add(*buttons, row_width=2)
        self.bot.send_message(chat_id, answer, reply_markup=markup)

    def _change_status_callback(self, call: types.CallbackQuery, data: str):
        # TODO: смена статуса
        chat_id = call.message.chat.id
        call_data = data.partition('/')
        task_id = call_data[0]
        new_state = call_data[2]
        if new_state == 'WAITING':
            new_state = 'WAITING_APPROVED'
        self.bot.edit_message_reply_markup(chat_id, call.message.id)

        try:
            response = requests.post(names.BASE_URL + 'tg/task/{}/{}'.format(task_id, chat_id),
                                     json={"state": new_state})
            if response.status_code != 200:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            self.bot.answer_callback_query(call.id, 'Невозможно выполнить операцию', False)

        self.bot.answer_callback_query(call.id, 'Статус изменён на: ' + new_state, False)
