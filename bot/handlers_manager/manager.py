"""Класс для управления обработчиками"""
from bot.handlers_manager.command_manager import CommandManager
from bot.handlers_manager.message_manager import MessageManager
from bot.handlers_manager.callback_manager import CallbackManager

__author__ = 'Обыденный И.В.'


class Manager:
    def __init__(self, bot):
        self.bot = bot
        self.command_manager = CommandManager(bot)
        self.message_manager = MessageManager(bot)
        self.callback_manager = CallbackManager(bot)

    def handle(self):
        self.command_manager.handle()
        self.message_manager.handle()
        self.callback_manager.handle()
