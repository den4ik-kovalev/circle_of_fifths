import math
from collections import deque
from typing import Optional

import flet as ft


class DefaultColors:
    circle_background = ft.colors.BLUE_GREY_200
    ring = ft.colors.BLUE_GREY_100
    chord = ft.colors.BLUE_GREY_700
    border = ft.colors.WHITE
    selected = ft.colors.BLACK87
    weak = ft.colors.BLUE_GREY_200


class AxisColors:
    tonic_strong = ft.colors.BLUE_GREY_900
    dominant_strong = ft.colors.GREEN_700
    subdominant_strong = ft.colors.BLUE_600
    tonic_weak = ft.colors.BLUE_GREY_700
    dominant_weak = ft.colors.GREEN_400
    subdominant_weak = ft.colors.BLUE_400

    chords = [
        tonic_strong,
        subdominant_strong,
        dominant_weak,
        tonic_weak,
        subdominant_weak,
        dominant_weak,
        tonic_weak,
        subdominant_weak,
        dominant_weak,
        tonic_weak,
        subdominant_weak,
        dominant_strong,
    ]

    borders = [
        ft.colors.RED,
        ft.colors.RED,
        ft.colors.ORANGE,
        ft.colors.YELLOW,
        ft.colors.YELLOW,
        ft.colors.WHITE,
        ft.colors.WHITE,
        ft.colors.WHITE,
        ft.colors.YELLOW,
        ft.colors.YELLOW,
        ft.colors.ORANGE,
        ft.colors.RED,
    ]


class CommonNotesColors:
    no = DefaultColors.weak
    root = ft.colors.RED_400
    third = ft.colors.BLUE_400
    fifth = ft.colors.GREEN_400
    root_third = ft.colors.BLUE_900
    root_fifth = ft.colors.RED_900
    third_fifth = ft.colors.GREEN_900

    major_selected = (
        [
            DefaultColors.selected, root,
            no, fifth, root,
            no, no, no,
            third, third, no,
            fifth
        ],
        [
            root_third, no,
            fifth, root_fifth, root,
            no, no, no,
            third, no, no,
            third_fifth
        ]
    )

    minor_selected = (
        [
            third_fifth, root_third,
            no, no, third,
            no, no, no,
            fifth, root_fifth, root,
            no
        ],
        [
            DefaultColors.selected, root,
            no, third, third,
            no, no, no,
            fifth, root, no,
            fifth
        ]
    )


class NegativeColors:
    # palette = [
    #     ft.colors.BLACK87,
    #     ft.colors.GREY_700,
    #     ft.colors.ORANGE_800,
    #     ft.colors.ORANGE_400,
    #     ft.colors.RED_800,
    #     ft.colors.RED_400,
    #     ft.colors.GREEN_800,
    #     ft.colors.GREEN_400,
    #     ft.colors.BLUE_800,
    #     ft.colors.BLUE_400,
    #     ft.colors.PURPLE_800,
    #     ft.colors.PURPLE_400
    # ]

    border_root = ft.colors.YELLOW_ACCENT_200

    palette = [
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
    ]

    major_selected = (
        [
            "black", "blue800",
            "blue400", "grey700", "green400",
            "red400", "purple400", "orange400",
            "orange800", "purple800", "red800",
            "green800"
        ],
        [
            "grey700", "blue400",
            "blue800", "black", "green800",
            "red800", "purple800", "orange800",
            "orange400", "purple400", "red400",
            "green400"
        ]
    )

    minor_selected = (
        [
            "grey700", "green400",
            "red400", "purple400", "orange400",
            "orange800", "purple800", "red800",
            "green800", "black", "blue800",
            "blue400"
        ],
        [
            "black", "green800",
            "red800", "purple800", "orange800",
            "orange400", "purple400", "red400",
            "green400", "grey700", "blue400",
            "blue800"
        ]
    )


CHORD_NAMES_FLAT = ("C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "B", "E", "A", "D", "G")
CHORD_NAMES_SHARP = ("C", "F", "A#", "D#", "G#", "C#", "F#", "B", "E", "A", "D", "G")
FLAT_2_SHARP = dict(zip(CHORD_NAMES_FLAT, CHORD_NAMES_SHARP))
SHARP_2_FLAT = dict(zip(CHORD_NAMES_SHARP, CHORD_NAMES_FLAT))


def main(page: ft.Page):

    def paint_default():
        for major_container, minor_container in zip(
            major_containers, minor_containers
        ):
            major_container.bgcolor = DefaultColors.chord
            minor_container.bgcolor = DefaultColors.chord
            major_container.border = ft.border.all(2, DefaultColors.border)
            minor_container.border = ft.border.all(2, DefaultColors.border)
        page.update()

    def paint_axis():
        for major_container, minor_container, bgcolor, border_color in zip(
            major_containers, minor_containers, AxisColors.chords, AxisColors.borders
        ):
            major_container.bgcolor = bgcolor
            minor_container.bgcolor = bgcolor
            major_container.border = ft.border.all(4, border_color)
            minor_container.border = ft.border.all(4, border_color)
        page.update()

    def paint_common_notes(is_major_selected: bool = True, shift: int = 0):
        if is_major_selected:
            major_colors, minor_colors = CommonNotesColors.major_selected
        else:
            major_colors, minor_colors = CommonNotesColors.minor_selected

        major_colors = deque(major_colors)
        minor_colors = deque(minor_colors)
        major_colors.rotate(shift)
        minor_colors.rotate(shift)

        for major_container, minor_container, major_color, minor_color in zip(
            major_containers, minor_containers, major_colors, minor_colors
        ):
            major_container.bgcolor = major_color
            minor_container.bgcolor = minor_color
        page.update()

    def paint_negative(is_major_selected: bool = True):
        if is_major_selected:
            major_colors, minor_colors = NegativeColors.major_selected
        else:
            major_colors, minor_colors = NegativeColors.minor_selected

        for major_container, minor_container, major_color, minor_color in zip(
            major_containers, minor_containers, major_colors, minor_colors
        ):
            major_container.bgcolor = major_color
            minor_container.bgcolor = minor_color

        if is_major_selected:
            major_containers[0].border = ft.border.all(8, NegativeColors.border_root)
            minor_containers[0].border = ft.border.all(2, DefaultColors.border)
        else:
            minor_containers[0].border = ft.border.all(8, NegativeColors.border_root)
            major_containers[0].border = ft.border.all(2, DefaultColors.border)

        page.update()

    def on_container_click(e: ft.ContainerTapEvent):
        is_major_selected = not e.control.data.endswith("m")
        chord_containers = major_containers if is_major_selected else minor_containers
        if radio_group.value == "a":
            while chord_containers[0] is not e.control:
                major_containers.rotate(1)
                minor_containers.rotate(1)
            for container, coords in zip(major_containers, MAJOR_COORDS):
                top, left = coords
                container.top = top
                container.left = left
            for container, coords in zip(minor_containers, MINOR_COORDS):
                top, left = coords
                container.top = top
                container.left = left
            paint_axis()
        elif radio_group.value == "c":
            shift = chord_containers.index(e.control)
            paint_common_notes(is_major_selected, shift)
        elif radio_group.value == "n":
            if e.control not in (major_containers[0], minor_containers[0]):
                return
            paint_negative(is_major_selected)
        else:
            pass
        page.update()

    def on_radio_group_change(e: Optional[ft.ControlEvent] = None):
        if e is None or e.control.value == "a":
            paint_axis()
        else:
            paint_default()

    def on_switch_sign_change(e: ft.ControlEvent):
        if e.control.value:
            for container in major_containers:
                chord = container.data
                text = container.content
                container.data = FLAT_2_SHARP[chord]
                text.value = FLAT_2_SHARP[chord]
            for container in minor_containers:
                chord = container.data[:-1]
                text = container.content
                container.data = FLAT_2_SHARP[chord] + "m"
                text.value = FLAT_2_SHARP[chord] + "m"
            e.control.label = "Sharps"
        else:
            for container in major_containers:
                chord = container.data
                text = container.content
                container.data = SHARP_2_FLAT[chord]
                text.value = SHARP_2_FLAT[chord]
            for container in minor_containers:
                chord = container.data[:-1]
                text = container.content
                container.data = SHARP_2_FLAT[chord] + "m"
                text.value = SHARP_2_FLAT[chord] + "m"
            e.control.label = "Flats"
        page.update()

    #-------------------------------------------------------------------------------#

    page.title = "Circle of Fifths"
    page.theme_mode = "dark"
    page.window_width = 840
    page.window_height = 660
    page.window_resizable = False
    page.window_maximizable = False
    page.padding = 10

    circle_bg_container_1 = ft.Container(
        width=600,
        height=600,
        bgcolor=DefaultColors.circle_background
    )

    circle_bg_container_2 = ft.Container(
        width=560,
        height=560,
        bgcolor=DefaultColors.ring,
        top=20,
        left=20,
        border_radius=280
    )

    circle_bg_container_3 = ft.Container(
        width=300,
        height=300,
        bgcolor=DefaultColors.circle_background,
        top=150,
        left=150,
        border_radius=150
    )

    # Центры по радиусу 225, в квадрате 450x450
    # Координаты точки на окружности: x = x0 + r*cosф, y = y0 + r*sinф
    # x0 = y0 = 300
    # ф ~ [0, 2П] - 12 равных промежутков
    # Радиус каждого кружочка - 50, в квадрате 100x100
    # Координаты левых верхних углов: x - 50, y - 50

    MAJOR_COORDS = []
    major_containers = deque()
    for i, chord in enumerate(CHORD_NAMES_FLAT):
        phi = 2 * math.pi / 12 * i
        phi += math.pi
        top = (300 + 250 * math.cos(phi) - 45)
        left = (300 + 250 * math.sin(phi) - 45)
        mcc = ft.Container(
            width=90,
            height=90,
            top=top,
            left=left,
            border_radius=45,
            alignment=ft.alignment.center,
            content=ft.Text(chord, size=32, weight="bold"),
            data=chord,
            on_click=on_container_click,
            animate_position=True,
            animate=True
        )
        MAJOR_COORDS.append((top, left))
        major_containers.append(mcc)

    MINOR_COORDS = []
    minor_containers = deque()
    for i, chord in enumerate(CHORD_NAMES_FLAT[9:12] + CHORD_NAMES_FLAT[0:9]):
        phi = 2 * math.pi / 12 * i
        phi += math.pi
        top = (300 + 175 * math.cos(phi) - 40)
        left = (300 + 175 * math.sin(phi) - 40)
        mcc = ft.Container(
            width=80,
            height=80,
            top=top,
            left=left,
            border_radius=40,
            alignment=ft.alignment.center,
            content=ft.Text(chord + "m", size=26, weight="bold"),
            data=chord + "m",
            on_click=on_container_click,
            animate_position=True,
            animate=True
        )
        MINOR_COORDS.append((top, left))
        minor_containers.append(mcc)

    circle_stack = ft.Stack(
        controls=[
            circle_bg_container_1,
            circle_bg_container_2,
            circle_bg_container_3,
            *major_containers,
            *minor_containers
        ]
    )

    switch_sign = ft.Switch(
        label="Flats",
        on_change=on_switch_sign_change
    )

    radio_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="a", label="Axis"),
            ft.Radio(value="c", label="Common"),
            ft.Radio(value="n", label="Negative")
        ]),
        value="a",
        on_change=on_radio_group_change
    )
    on_radio_group_change()

    controls_column = ft.Column(
        controls=[switch_sign, radio_group]
    )

    main_row = ft.Row(
        controls=[circle_stack, controls_column]
    )

    page.add(main_row)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)