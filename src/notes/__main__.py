import flet as ft

from .notes import Notes


def main(page: ft.Page):
    Notes(page)


ft.app(main)
