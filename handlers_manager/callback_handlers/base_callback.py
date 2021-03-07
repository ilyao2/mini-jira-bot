"""Основной обработчик колбэков"""
import telebot

__author__ = 'Обыденный И.В.'


def handle(bot: telebot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        bot.send_message(call.message.chat.id, call.data)
        # TODO: Обработчик, парсер call.data
