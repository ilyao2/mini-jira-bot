"""Модуль для управления обработчиками"""
from handlers_manager import command_handlers, message_handlers, callback_handlers

__author__ = 'Обыденный И.В.'


def handle(bot):
    command_handlers.handle(bot)
    message_handlers.handle(bot)
    callback_handlers.handle(bot)
