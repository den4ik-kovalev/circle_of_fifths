from __future__ import annotations
from collections import deque
from enum import Enum, auto
from typing import Callable

import flet as ft

from chord import Chord
from utils import Trigonometry


class ChordContainer(ft.UserControl):

    def __init__(self, chord: Chord, cb_click: Callable) -> None:
        super(ChordContainer, self).__init__(animate_position=True)
        self.chord = chord
        self._cb_click = cb_click

    @property
    def control(self) -> ft.Container:
        return self.controls[0]

    def build(self) -> ft.Container:
        return ft.Container(
            width=(90 if self.chord.is_major else 80),
            height=(90 if self.chord.is_major else 80),
            border=ft.border.all(2, ft.colors.WHITE),
            border_radius=(45 if self.chord.is_major else 40),
            alignment=ft.alignment.center,
            content=ft.Text(
                value=self.chord.flat_name,
                size=(32 if self.chord.is_major else 26),
                weight=ft.FontWeight.BOLD
            ),
            on_click=self._on_click,
            animate=True
        )

    def _on_click(self, e: ft.ControlEvent):
        self._cb_click(self)


class SharpFlatSwitch(ft.UserControl):

    class State(Enum):
        FLATS = auto()  # Бемоли
        SHARPS = auto()  # Диезы

    def __init__(self, cb_change: Callable):
        super(SharpFlatSwitch, self).__init__()
        self.cb_change = cb_change

    @property
    def control(self) -> ft.Switch:
        return self.controls[0]

    @property
    def state(self) -> State:
        return self.State.SHARPS if self.control.value else self.State.FLATS

    def build(self) -> ft.Switch:
        return ft.Switch(
            label="Flats",
            on_change=self._on_change
        )

    def _on_change(self, e: ft.ControlEvent):
        self.control.label = "Flats" if self.state == self.State.FLATS else "Sharps"
        self.update()
        self.cb_change(self.state)


class OptionsRadioGroup(ft.UserControl):

    class State(Enum):
        AXIS = auto()  # Функциональные оси
        COMMON = auto()  # Общие ноты
        NEGATIVE = auto()  # Негативная гармония

    def __init__(self, cb_change: Callable):
        super(OptionsRadioGroup, self).__init__()
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


class Circle(ft.UserControl):

    class Mode(Enum):
        AXIS = auto()  # Функциональные оси
        COMMON = auto()  # Общие ноты
        NEGATIVE = auto()  # Негативная гармония

    def __init__(self):

        super(Circle, self).__init__()
        self._mode = self.Mode.AXIS

        major_chords, minor_chors = Chord.all_triads()
        # В этих контейнерах под индексом 0 всегда верхний контейнер
        self._major_containers = deque([ChordContainer(c, cb_click=self._on_container_click) for c in major_chords])
        self._minor_containers = deque([ChordContainer(c, cb_click=self._on_container_click) for c in minor_chors])

        circle_coords = Trigonometry.circle_coords(
            center=(300, 300),
            r=250,
            n=12
        )
        circle_coords = deque(circle_coords)
        circle_coords.rotate(6)
        for major_container, coords in zip(self._major_containers, circle_coords):
            x, y = coords
            major_container.top = x - 45
            major_container.left = y - 45

        circle_coords = Trigonometry.circle_coords(
            center=(300, 300),
            r=175,
            n=12
        )
        circle_coords = deque(circle_coords)
        circle_coords.rotate(6)
        for minor_container, coords in zip(self._minor_containers, circle_coords):
            x, y = coords
            minor_container.top = x - 40
            minor_container.left = y - 40

    @property
    def chord_containers(self):
        return self._major_containers + self._minor_containers

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

        return ft.Stack([
            layer_1,
            layer_2,
            layer_3,
            *self._major_containers,
            *self._minor_containers
        ])

    def set_mode(self, mode: Circle.Mode) -> None:
        self._mode = mode
        if mode == self.Mode.AXIS:
            self.paint_axis()
        else:
            self.paint_grey()

    def set_sharps(self) -> None:
        for container in self.chord_containers:
            container.control.content.value = container.chord.sharp_name
            container.update()

    def set_flats(self) -> None:
        for container in self.chord_containers:
            container.control.content.value = container.chord.flat_name
            container.update()

    def paint_grey(self) -> None:
        for container in self.chord_containers:
            container.control.bgcolor = ft.colors.BLUE_GREY_200
            container.update()

    def paint_axis(self) -> None:

        major_colors = deque([
            ft.colors.BLUE_GREY_900,
            ft.colors.BLUE_GREY_700,
            ft.colors.GREY_600
        ])
        for container in self._major_containers:
            container.control.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            container.update()

        minor_colors = deque([
            ft.colors.BLUE_GREY_900,
            ft.colors.BLUE_GREY_700,
            ft.colors.GREY_600
        ])
        for container in self._minor_containers:
            container.control.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            container.update()

    def paint_common(self, container: ChordContainer) -> None:

        if container.chord.is_major:
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
            major_colors.rotate(self._major_containers.index(container))
            minor_colors.rotate(self._major_containers.index(container))
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
            major_colors.rotate(self._minor_containers.index(container))
            minor_colors.rotate(self._minor_containers.index(container))

        for container in self._major_containers:
            container.control.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            container.update()

        for container in self._minor_containers:
            container.control.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            container.update()

    def paint_negative(self, container: ChordContainer) -> None:

        if container.chord.is_major:
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
            major_colors.rotate(self._major_containers.index(container))
            minor_colors.rotate(self._major_containers.index(container))
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
            major_colors.rotate(self._minor_containers.index(container))
            minor_colors.rotate(self._minor_containers.index(container))

        for container in self._major_containers:
            container.control.bgcolor = major_colors[0]
            major_colors.rotate(-1)
            container.update()

        for container in self._minor_containers:
            container.control.bgcolor = minor_colors[0]
            minor_colors.rotate(-1)
            container.update()

    def _on_container_click(self, container: ChordContainer) -> None:
        if self._mode == self.Mode.AXIS:
            self._rotate_to(container)
            self.paint_axis()
        elif self._mode == self.Mode.COMMON:
            self.paint_common(container)
        elif self._mode == self.Mode.NEGATIVE:
            self.paint_negative(container)

    def _rotate_to(self, container: ChordContainer) -> None:

        prev_params = [(c.top, c.left, c.control.bgcolor) for c in self.chord_containers]

        if container.chord.is_major:
            while self._major_containers[0] is not container:
                self._major_containers.rotate()
                self._minor_containers.rotate()
        else:
            while self._minor_containers[0] is not container:
                self._major_containers.rotate()
                self._minor_containers.rotate()

        for container, params in zip(self.chord_containers, prev_params):
            top, left, bgcolor = params
            container.top = top
            container.left = left
            container.control.bgcolor = bgcolor
            container.update()
