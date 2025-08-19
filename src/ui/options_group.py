from enum import Enum, auto
from typing import Callable

import flet as ft


class OptionsGroup(ft.UserControl):

    class State(Enum):
        AXIS = auto()  # Функциональные оси
        COMMON = auto()  # Общие ноты
        NEGATIVE = auto()  # Негативная гармония

    def __init__(self, cb_change: Callable):
        super(OptionsGroup, self).__init__()
        self.cb_change = cb_change

    def build(self) -> ft.RadioGroup:
        return ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="axis", label="Functional Axis"),
                ft.Radio(value="common", label="Common Notes"),
                ft.Radio(value="negative", label="Negative Harmony")
            ]),
            value="axis",
            on_change=self._on_change
        )

    def _on_change(self, e: ft.ControlEvent):
        value = e.control.value
        if value == "axis":
            self.cb_change(self.State.AXIS)
        elif value == "common":
            self.cb_change(self.State.COMMON)
        elif value == "negative":
            self.cb_change(self.State.NEGATIVE)
