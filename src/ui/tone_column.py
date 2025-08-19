from typing import Callable

import flet as ft

from src.core.tone import Tone


class ToneColumn(ft.UserControl):

    def __init__(self, cb_change: Callable):
        super(ToneColumn, self).__init__()
        self.cb_change = cb_change

    @property
    def checkboxes(self) -> list[ft.Checkbox]:
        return self.controls[0].controls

    def build(self) -> ft.Column:
        checkboxes = [
            ft.Checkbox(
                label=tone.flat_name,
                data=tone,
                on_change=self._on_change
            )
            for tone in Tone.twelve_tone_row()
        ]
        return ft.Column(checkboxes, spacing=0)

    def set_sharps(self) -> None:
        for checkbox in self.checkboxes:
            tone = checkbox.data
            checkbox.label = tone.sharp_name
            checkbox.update()

    def set_flats(self) -> None:
        for checkbox in self.checkboxes:
            tone = checkbox.data
            checkbox.label = tone.flat_name
            checkbox.update()

    def _on_change(self, e: ft.ControlEvent):
        self.cb_change([cb.data for cb in self.checkboxes if cb.value])
