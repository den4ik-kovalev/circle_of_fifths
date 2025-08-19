from __future__ import annotations
from collections import deque
from enum import Enum, auto

import flet as ft

from src.core.chord import MajorTriad, MinorTriad
from src.core.tone import Tone
from src.ui.chord_bubble import ChordBubble
from src.utils.trigonometry import Trigonometry


class Circle(ft.UserControl):

    class Mode(Enum):
        AXIS = auto()  # Функциональные оси
        COMMON = auto()  # Общие ноты
        NEGATIVE = auto()  # Негативная гармония

    def __init__(self):

        super(Circle, self).__init__()
        self._mode = self.Mode.AXIS

        self._degree_container: ft.Container = ...

        # В этих deque под индексом 0 всегда верхний контейнер
        self._major_bubbles = deque([
            ChordBubble(
                c,
                cb_click=self._on_bubble_click,
                cb_hover_begin=self._on_bubble_hover_begin,
                cb_hover_end=self._on_bubble_hover_end
            )
            for c in MajorTriad.circle()
        ])
        self._minor_bubbles = deque([
            ChordBubble(
                c,
                cb_click=self._on_bubble_click,
                cb_hover_begin=self._on_bubble_hover_begin,
                cb_hover_end=self._on_bubble_hover_end
            )
            for c in MinorTriad.circle()
        ])

        circle_coords = Trigonometry.circle_coords(
            center=(300, 300),
            r=250,
            n=12
        )
        circle_coords = deque(circle_coords)
        circle_coords.rotate(6)
        for major_bubble, coords in zip(self._major_bubbles, circle_coords):
            x, y = coords
            major_bubble.top = x - 45
            major_bubble.left = y - 45

        circle_coords = Trigonometry.circle_coords(
            center=(300, 300),
            r=175,
            n=12
        )
        circle_coords = deque(circle_coords)
        circle_coords.rotate(6)
        for minor_bubble, coords in zip(self._minor_bubbles, circle_coords):
            x, y = coords
            minor_bubble.top = x - 40
            minor_bubble.left = y - 40

    @property
    def chord_bubbles(self):
        return self._major_bubbles + self._minor_bubbles

    def build(self) -> ft.Stack:

        layer_1 = ft.Container(
            width=600,
            height=600,
            bgcolor=ft.colors.BLUE_GREY_200
        )

        layer_2 = ft.Container(
            width=560,
            height=560,
            bgcolor=ft.colors.BLUE_GREY_100,
            top=20,
            left=20,
            border_radius=280
        )

        layer_3 = ft.Container(
            width=300,
            height=300,
            bgcolor=ft.colors.BLUE_GREY_200,
            top=150,
            left=150,
            border_radius=150
        )

        self._degree_container = ft.Container(
            width=60,
            height=60,
            border=ft.border.all(2, ft.colors.BLUE_GREY_900),
            border_radius=35,
            alignment=ft.alignment.center,
            content=ft.Text(
                value="",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_GREY_900
            ),
            top=(300-30),
            left=(300-30),
            opacity=0.5,
            visible=False
        )

        return ft.Stack([
            layer_1,
            layer_2,
            layer_3,
            self._degree_container,
            *self._major_bubbles,
            *self._minor_bubbles
        ])

    def set_mode(self, mode: Circle.Mode) -> None:
        self._mode = mode
        if mode == self.Mode.AXIS:
            self.paint_axis()
        else:
            self.paint_grey()

    def set_sharps(self) -> None:
        for bubble in self.chord_bubbles:
            bubble.container.content.value = bubble.chord.sharp_name
            bubble.container.tooltip = " ".join([t.sharp_name for t in bubble.chord.tones()])
            bubble.update()

    def set_flats(self) -> None:
        for bubble in self.chord_bubbles:
            bubble.container.content.value = bubble.chord.flat_name
            bubble.container.tooltip = " ".join([t.flat_name for t in bubble.chord.tones()])
            bubble.update()

    def paint_grey(self) -> None:
        for bubble in self.chord_bubbles:
            bubble.container.bgcolor = ft.colors.BLUE_GREY_200
            bubble.update()

    def paint_axis(self) -> None:

        major_colors = deque([
            ft.colors.BLUE_GREY_900,
            ft.colors.BLUE_GREY_700,
            ft.colors.GREY_600
        ])
        for bubble in self._major_bubbles:
            bubble.container.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            bubble.update()

        minor_colors = deque([
            ft.colors.BLUE_GREY_900,
            ft.colors.BLUE_GREY_700,
            ft.colors.GREY_600
        ])
        for bubble in self._minor_bubbles:
            bubble.container.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            bubble.update()

    def paint_common(self, main: ChordBubble) -> None:

        if isinstance(main.chord, MajorTriad):
            major_colors = deque([
                ft.colors.BLACK,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300
            ])
            minor_colors = deque([
                ft.colors.RED_600,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_600,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_600
            ])
            major_colors.rotate(self._major_bubbles.index(main))
            minor_colors.rotate(self._major_bubbles.index(main))
        else:
            major_colors = deque([
                ft.colors.RED_600,
                ft.colors.RED_600,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_600,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200
            ])
            minor_colors = deque([
                ft.colors.BLACK,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300,
                ft.colors.RED_300,
                ft.colors.BLUE_GREY_200,
                ft.colors.RED_300
            ])
            major_colors.rotate(self._minor_bubbles.index(main))
            minor_colors.rotate(self._minor_bubbles.index(main))

        for bubble in self._major_bubbles:
            bubble.container.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            bubble.update()

        for bubble in self._minor_bubbles:
            bubble.container.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            bubble.update()

    def paint_negative(self, main: ChordBubble) -> None:

        if isinstance(main.chord, MajorTriad):
            major_colors = deque([
                ft.colors.BLACK,
                ft.colors.BLUE_800,
                ft.colors.BLUE_400,
                ft.colors.GREY_700,
                ft.colors.GREEN_400,
                ft.colors.RED_400,
                ft.colors.PURPLE_400,
                ft.colors.ORANGE_400,
                ft.colors.ORANGE_800,
                ft.colors.PURPLE_800,
                ft.colors.RED_800,
                ft.colors.GREEN_800
            ])
            minor_colors = deque([
                ft.colors.GREY_700,
                ft.colors.BLUE_400,
                ft.colors.BLUE_800,
                ft.colors.BLACK,
                ft.colors.GREEN_800,
                ft.colors.RED_800,
                ft.colors.PURPLE_800,
                ft.colors.ORANGE_800,
                ft.colors.ORANGE_400,
                ft.colors.PURPLE_400,
                ft.colors.RED_400,
                ft.colors.GREEN_400
            ])
            major_colors.rotate(self._major_bubbles.index(main))
            minor_colors.rotate(self._major_bubbles.index(main))
        else:
            major_colors = deque([
                ft.colors.GREY_700,
                ft.colors.GREEN_400,
                ft.colors.RED_400,
                ft.colors.PURPLE_400,
                ft.colors.ORANGE_400,
                ft.colors.ORANGE_800,
                ft.colors.PURPLE_800,
                ft.colors.RED_800,
                ft.colors.GREEN_800,
                ft.colors.BLACK,
                ft.colors.BLUE_800,
                ft.colors.BLUE_400
            ])
            minor_colors = deque([
                ft.colors.BLACK,
                ft.colors.GREEN_800,
                ft.colors.RED_800,
                ft.colors.PURPLE_800,
                ft.colors.ORANGE_800,
                ft.colors.ORANGE_400,
                ft.colors.PURPLE_400,
                ft.colors.RED_400,
                ft.colors.GREEN_400,
                ft.colors.GREY_700,
                ft.colors.BLUE_400,
                ft.colors.BLUE_800
            ])
            major_colors.rotate(self._minor_bubbles.index(main))
            minor_colors.rotate(self._minor_bubbles.index(main))

        for bubble in self._major_bubbles:
            bubble.container.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            bubble.update()

        for bubble in self._minor_bubbles:
            bubble.container.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            bubble.update()

    def highlight_by_tones(self, tones: list[Tone]):

        if not tones:
            for bubble in self.chord_bubbles:
                bubble.highlight_off()
            return

        for bubble in self.chord_bubbles:
            if all([tone in bubble.chord.tones() for tone in tones]):
                bubble.highlight_on()
            else:
                bubble.highlight_off()
        return

    def set_degrees_for_major_tonic(self) -> None:
        for bubble in self.chord_bubbles:
            bubble.degree = None
        self._major_bubbles[0].degree = "I"
        self._major_bubbles[1].degree = "IV"
        self._major_bubbles[-1].degree = "V"
        self._minor_bubbles[0].degree = "vi"
        self._minor_bubbles[1].degree = "ii"
        self._minor_bubbles[-1].degree = "iii"

    def set_degrees_for_minor_tonic(self) -> None:
        for bubble in self.chord_bubbles:
            bubble.degree = None
        self._major_bubbles[0].degree = "III"
        self._major_bubbles[1].degree = "VI"
        self._major_bubbles[-1].degree = "VII"
        self._minor_bubbles[0].degree = "i"
        self._minor_bubbles[1].degree = "iv"
        self._minor_bubbles[-1].degree = "v"

    def _rotate_to(self, bubble: ChordBubble) -> None:

        prev_params = [(c.top, c.left, c.container.bgcolor) for c in self.chord_bubbles]

        if isinstance(bubble.chord, MajorTriad):
            while self._major_bubbles[0] is not bubble:
                self._major_bubbles.rotate()
                self._minor_bubbles.rotate()
        else:
            while self._minor_bubbles[0] is not bubble:
                self._major_bubbles.rotate()
                self._minor_bubbles.rotate()

        for bubble, params in zip(self.chord_bubbles, prev_params):
            top, left, bgcolor = params
            bubble.top = top
            bubble.left = left
            bubble.container.bgcolor = bgcolor
            bubble.update()

    def _show_degree(self, degree: str) -> None:
        self._degree_container.content.value = degree
        self._degree_container.visible = True
        self._degree_container.update()

    def _hide_degree(self) -> None:
        self._degree_container.content.value = ""
        self._degree_container.visible = False
        self._degree_container.update()

    def _on_bubble_click(self, bubble: ChordBubble) -> None:

        if self._mode == self.Mode.AXIS:
            self._rotate_to(bubble)
            self.paint_axis()
        elif self._mode == self.Mode.COMMON:
            self.paint_common(bubble)
        elif self._mode == self.Mode.NEGATIVE:
            self.paint_negative(bubble)

        if isinstance(bubble.chord, MajorTriad):
            self.set_degrees_for_major_tonic()
        else:
            self.set_degrees_for_minor_tonic()

    def _on_bubble_hover_begin(self, bubble: ChordBubble) -> None:
        if self._mode != self.Mode.AXIS:
            return
        if bubble.degree:
            self._show_degree(bubble.degree)
        else:
            self._hide_degree()

    def _on_bubble_hover_end(self, bubble: ChordBubble) -> None:
        if self._mode != self.Mode.AXIS:
            return
        self._hide_degree()
