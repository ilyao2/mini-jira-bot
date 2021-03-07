"""Модуль для управления обработчиками"""
from handlers_manager import command_handlers

__author__ = 'Обыденный И.В.'


def handle(bot):
    command_handlers.start.handle(bot)
