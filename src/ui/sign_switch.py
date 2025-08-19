from enum import Enum, auto
from typing import Callable

import flet as ft


class SignSwitch(ft.UserControl):

    class State(Enum):
        FLATS = auto()  # Бемоли
        SHARPS = auto()  # Диезы

    def __init__(self, cb_change: Callable):
        super(SignSwitch, self).__init__()
        self.cb_change = cb_change

    @property
    def switch(self) -> ft.Switch:
        return self.controls[0]

    @property
    def state(self) -> State:
        return self.State.SHARPS if self.switch.value else self.State.FLATS

    def build(self) -> ft.Switch:
        return ft.Switch(
            label="Flats",
            on_change=self._on_change
        )

    def _on_change(self, e: ft.ControlEvent):
        self.switch.label = "Flats" if self.state == self.State.FLATS else "Sharps"
        self.switch.update()
        self.cb_change(self.state)
