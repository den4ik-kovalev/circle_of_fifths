import flet as ft

from ui import Circle, SharpFlatSwitch, OptionsRadioGroup


def main(page: ft.Page):

    def on_switch_change(state: SharpFlatSwitch.State) -> None:
        if state == SharpFlatSwitch.State.SHARPS:
            circle.set_sharps()
        else:
            circle.set_flats()

    def on_radio_change(state: OptionsRadioGroup.State) -> None:
        if state == OptionsRadioGroup.State.AXIS:
            circle.set_mode(Circle.Mode.AXIS)
        elif state == OptionsRadioGroup.State.COMMON:
            circle.set_mode(Circle.Mode.COMMON)
        elif state == OptionsRadioGroup.State.NEGATIVE:
            circle.set_mode(Circle.Mode.NEGATIVE)

    page.title = "Circle of Fifths"
    page.theme_mode = "dark"
    page.window_width = 840
    page.window_height = 660
    page.window_resizable = False
    page.window_maximizable = False
    page.padding = 10

    circle = Circle()
    switch = SharpFlatSwitch(cb_change=on_switch_change)
    radio = OptionsRadioGroup(cb_change=on_radio_change)

    page.add(
        ft.Row(
            controls=[
                circle,
                ft.Column([switch, radio])
            ],
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )
    circle.set_flats()
    circle.paint_axis()

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
