import flet as ft

from src.core.tone import Tone

from src.ui.circle import Circle
from src.ui.options_group import OptionsGroup
from src.ui.sign_switch import SignSwitch
from src.ui.tone_column import ToneColumn


def main(page: ft.Page):

    def on_switch_change(state: SignSwitch.State) -> None:
        if state == SignSwitch.State.SHARPS:
            circle.set_sharps()
            tone_column.set_sharps()
        else:
            circle.set_flats()
            tone_column.set_flats()

    def on_radio_change(state: OptionsGroup.State) -> None:
        if state == OptionsGroup.State.AXIS:
            circle.set_mode(Circle.Mode.AXIS)
        elif state == OptionsGroup.State.COMMON:
            circle.set_mode(Circle.Mode.COMMON)
        elif state == OptionsGroup.State.NEGATIVE:
            circle.set_mode(Circle.Mode.NEGATIVE)

    def on_checkbox_change(tones: list[Tone]) -> None:
        circle.highlight_by_tones(tones)

    page.title = "Circle of Fifths"
    page.theme_mode = "dark"
    page.window_width = 840
    page.window_height = 660
    page.window_resizable = False
    page.window_maximizable = False
    page.padding = 10

    circle = Circle()
    switch = SignSwitch(cb_change=on_switch_change)
    radio = OptionsGroup(cb_change=on_radio_change)
    tone_column = ToneColumn(cb_change=on_checkbox_change)

    page.add(
        ft.Row(
            controls=[
                circle,
                ft.Column([
                    switch,
                    ft.Container(width=195, height=1, bgcolor="white"),
                    radio,
                    ft.Container(width=195, height=1, bgcolor="white"),
                    tone_column
                ])
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )
    circle.set_flats()
    circle.paint_axis()
    circle.set_degrees_for_major_tonic()

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
