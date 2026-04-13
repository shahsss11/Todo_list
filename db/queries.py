tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
"""

insert_task = 'INSERT INTO tasks(task) VALUES(?)'

select_all_tasks = 'SELECT * FROM tasks'

update_task = 'UPDATE tasks SET task = ? WHERE id = ?'

delete_task = 'DELETE FROM tasks WHERE id = ?'