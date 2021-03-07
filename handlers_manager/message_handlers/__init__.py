"""Модуль для управления обработчиками входящих сообщений"""
from handlers_manager.message_handlers import base_message, tasks_list, show_web, create_task

__author__ = 'Обыденный И.В.'


def handle(bot):
    create_task.handle(bot)
    tasks_list.handle(bot)
    show_web.handle(bot)
    base_message.handle(bot)
