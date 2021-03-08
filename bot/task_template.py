"""Класс шаблона задачи"""
from typing import Optional
from datetime import date

__author__ = 'Обыденный И.В.'


class TaskTemplate:
    """Класс для работы с шаблонами задач"""
    class State:
        title_input = 0
        reporter_input = 1
        description_input = 2
        deadline_input = 3
        ready = 5

    def __init__(self):
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.reporter_uuid: Optional[str] = None
        self.deadline: Optional[date] = None
        self.state: int = TaskTemplate.State.title_input
