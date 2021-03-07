"""Модуль для управления обработчиками входящих сообщений"""
from handlers_manager.message_handlers import base_message

__author__ = 'Обыденный И.В.'


def handle(bot):
    base_message.handle(bot)
