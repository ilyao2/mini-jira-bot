"""Модуль для уаправления обработчиками команд"""
from handlers_manager.command_handlers import auth, start

__author__ = 'Обыденный И.В.'


def handle(bot):
    auth.handle(bot)
    start.handle(bot)
