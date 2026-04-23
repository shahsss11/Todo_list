import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = "ToDo App"
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    filter_type = "all"

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        on_click=toggle_theme,
        tooltip="Сменить тему"
    )

    def load_tasks():
        task_list.controls.clear()
        tasks = list(main_db.get_tasks(filter_type=filter_type))

        if len(tasks) == 0:
            task_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [ft.Text(" Список задач пуст", )],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    
                )
            )
        else:
            task_list.controls.append(
                ft.Text(
                    f" Всего задач: {len(tasks)}",
                )
            )

            for task_id, task_text, completed in tasks:
                task_list.controls.append(
                    view_tasks(task_id, task_text, completed)
                )

        page.update()

    def view_tasks(task_id, task_text, completed):
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        task_field = ft.TextField(
            value=task_text,
            read_only=True,
            expand=True,
            border="none",
            on_submit=lambda e: save_task(e)
        )

        def toggle_edit(e):
            task_field.read_only = not task_field.read_only
            page.update()

        def save_task(e):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            load_tasks()

        return ft.Container(
            content=ft.Row(
                [
                    checkbox,
                    task_field,
                    ft.IconButton(ft.Icons.EDIT, on_click=toggle_edit),
                    ft.IconButton(ft.Icons.SAVE, on_click=save_task)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        )

    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()

    def add_task(e):
        if task_input.value:
            main_db.add_task(task=task_input.value)
            task_input.value = ""
            load_tasks()

    task_input = ft.TextField(
        label="Введите задачу...",
        expand=True,
        on_submit=add_task
    )

    add_button = ft.ElevatedButton(
        "Добавить",
        icon=ft.Icons.ADD,
        on_click=add_task
    )


    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_tasks()

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter("all"), icon=ft.Icons.LIST),
            ft.ElevatedButton("В работе", on_click=lambda e: set_filter("uncompleted"), icon=ft.Icons.HOURGLASS_TOP),
            ft.ElevatedButton("Готово", on_click=lambda e: set_filter("completed"), icon=ft.Icons.DONE),
            ft.ElevatedButton('Удалить завершенные', icon=ft.Icons.DELETE, on_click=lambda e: (main_db.delete_completed_tasks() , load_tasks()), icon_color=ft.Colors.RED_900)

        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    page.add(
        ft.Row(
            [
                ft.Text(" ToDo App", ),
                theme_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),

        ft.Text("Управляй задачами "),

        ft.Row([task_input, add_button]),

        ft.Container(),

        ft.Text("Фильтры", ),

        filter_buttons,

        ft.Container(),

        task_list
    )

    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)