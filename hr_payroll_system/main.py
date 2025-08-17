import flet as ft
from views.main_view import MainView

def main(page: ft.Page):
    page.title = "HR & Payroll System"
    page.window_width = 1200
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    main_view = MainView()
    page.add(main_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
