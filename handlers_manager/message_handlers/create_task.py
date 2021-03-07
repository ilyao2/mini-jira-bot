"""Основной обработчик сообщений"""
import telebot
from handlers_manager import names
from handlers_manager.message_handlers.base_message import msg_dict

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    def answer(msg):
        bot.send_message(msg.chat.id, names.CREATE_TASK)
    msg_dict[names.CREATE_TASK] = answer
