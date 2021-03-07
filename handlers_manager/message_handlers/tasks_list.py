"""Основной обработчик сообщений"""
import telebot
from  telebot import types
from handlers_manager import names
from handlers_manager.message_handlers.base_message import msg_dict

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    def answer(msg):
        # TODO: задачи сортируются по дате
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заголовок задачи 1', callback_data='task: 1'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 2', callback_data='task: 2'))
        markup.add(types.InlineKeyboardButton('Заголовок задачи 3', callback_data='task: 3'))
        bot.send_message(msg.chat.id, names.TASKS_LIST, reply_markup=markup)
    msg_dict[names.TASKS_LIST] = answer
