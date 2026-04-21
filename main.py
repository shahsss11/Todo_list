import flet as ft
from db import main_db 


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    filter_type = 'all'

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(view_tasks(
                task_id=task_id,
                task_text=task_text,
                completed=completed
                ))


    def view_tasks(task_id, task_text, completed=None):
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value)
            )

        task_field = ft.TextField(read_only=True, value=task_text, expand=True)

        def enable_edit(e):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True


        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(e):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)


        return ft.Row([checkbox, task_field, edit_button, save_button])
    
    def toggle_task(task_id, is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()

    def add_task(e):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            print(f'Задача {task} добавлена! Его ID - {task_id}')
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task))
            task_input.value = None


    task_input = ft.TextField(label="Введите задачу", expand=True, on_submit=add_task)

    task_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()
        

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.BLACK),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.WATCH, icon_color=ft.Colors.YELLOW_900),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN_900)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    send_task = ft.Row([task_input, task_button])

    page.add(send_task, filter_buttons, task_list)
    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)