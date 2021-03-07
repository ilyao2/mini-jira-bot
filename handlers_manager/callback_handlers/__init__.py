"""Модуль для уаправления обработчиками колбэков (Для обработки инлайн кнопок)"""
from handlers_manager.callback_handlers import base_callback

__author__ = 'Обыденный И.В.'


def handle(bot):
    base_callback.handle(bot)
