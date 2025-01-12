import sqlite3
from datetime import datetime
from flask import *

app = Flask(__name__)

def init_db():
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date_created TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Р’ РїСЂРѕС†РµСЃСЃРµ',
    completed BOOLEAN NOT NULL DEFAULT 0)''')
    connection.commit()
    connection.close()

@app.route('/')
def index():
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    connection.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    date_created = datetime.now()
    if title:
        connection = sqlite3.connect("task_manager.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tasks(title, date_created) VALUES (?,?)', (title, date_created))
        connection.commit()
        connection.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute('UPDATE tasks SET completed = 1, status = "Completed" WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    new_title = request.form['title']
    status = request.form['status']
    if new_title:
        connection = sqlite3.connect("task_manager.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE tasks SET title = ?, status = ? WHERE id = ?', (new_title, status, task_id))
        connection.commit()
        connection.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    connection = sqlite3.connect("task_manager.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

