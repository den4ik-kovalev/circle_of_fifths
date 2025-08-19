from typing import Callable, Optional

import flet as ft

from src.core.chord import Chord, MajorTriad


class ChordBubble(ft.UserControl):

    def __init__(
            self,
            chord: Chord,
            cb_click: Callable,
            cb_hover_begin: Callable,
            cb_hover_end: Callable
    ) -> None:

        super(ChordBubble, self).__init__(animate_position=666)
        self._chord = chord
        self.degree: Optional[str] = None
        self.cb_click = cb_click
        self.cb_hover_begin = cb_hover_begin
        self.cb_hover_end = cb_hover_end

    @property
    def chord(self) -> Chord:
        return self._chord

    @property
    def container(self) -> ft.Container:
        return self.controls[0]

    def build(self) -> ft.Container:
        big = isinstance(self._chord, MajorTriad)
        return ft.Container(
            width=(90 if big else 80),
            height=(90 if big else 80),
            border=ft.border.all(2, ft.colors.WHITE),
            border_radius=(45 if big else 40),
            alignment=ft.alignment.center,
            content=ft.Text(
                value=self._chord.flat_name,
                size=(32 if big else 26),
                weight=ft.FontWeight.BOLD,
                data={}
            ),
            on_click=self._on_click,
            on_hover=self._on_hover,
            animate=666
        )

    def highlight_on(self) -> None:
        self.container.border = ft.border.all(8, ft.colors.YELLOW)
        self.container.update()

    def highlight_off(self) -> None:
        self.container.border = ft.border.all(2, ft.colors.WHITE)
        self.container.update()

    def _on_click(self, e: ft.ControlEvent) -> None:
        self.cb_click(self)

    def _on_hover(self, e: ft.ControlEvent) -> None:
        if e.data == "true":
            self.cb_hover_begin(self)
        else:
            self.cb_hover_end(self)
