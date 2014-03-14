from flask import render_template, request, redirect, url_for
from app import app, connection
from mongokit import ObjectId

global actual_state
actual_state = 'show_all'


def get_todos(state):
    global actual_state
    actual_state = state
    todos = {}
    todos['all_todos'] = list(connection.Todo.find())
    todos['active_todos'] = [td for td in todos['all_todos'] if not td['completed']]
    todos['completed_todos'] = [td for td in todos['all_todos'] if td['completed']]
    todos['clear_completed'] = len(todos['completed_todos'])
    todos['items_left'] = len(todos['active_todos'])
    return todos

@app.route('/')
def show_all():
    # global actual_state
    # actual_state = 'show_all'
    # db_todos = list(connection.Todo.find())
    # clear_completed = len(list(connection.Todo.find({'completed': True})))

    td = get_todos('show_all')

    return render_template('home.html', selected='all', todos=td['all_todos'], clear_completed=td['clear_completed'],
                           items_left=td['items_left'])


@app.route('/active')
def show_active():
    # global actual_state
    # actual_state = 'show_active'
    # active_todos = list(connection.Todo.find({'completed': False}))
    # clear_completed = len(list(connection.Todo.find({'completed': True})))

    td = get_todos('show_active')

    return render_template('home.html', selected='active', todos=td['active_todos'], clear_completed=td['clear_completed'],
                           items_left=td['items_left'])


@app.route('/completed')
def show_completed():
    # global actual_state
    # actual_state = 'show_completed'
    # completed_todos = list(connection.Todo.find({'completed': True}))
    # clear_completed = len(list(connection.Todo.find({'completed': True})))

    td = get_todos('show_completed')

    return render_template('home.html', selected='completed', todos=td['completed_todos'], clear_completed=td['clear_completed'],
                           items_left=td['items_left'])


@app.route('/add', methods=['POST'])
def add_todo():
    global actual_state
    new_todo = connection.Todo()
    new_todo.title = request.form['todo']
    new_todo.save()
    return redirect(url_for(actual_state))


@app.route('/delete', methods=['POST'])
def delete_todo():
    global actual_state
    connection.Todo.find_one({'_id': ObjectId(request.form['id'])}).delete()
    return redirect(url_for(actual_state))


@app.route('/delete_completed', methods=['POST'])
def delete_completed():
    global actual_state

    for td in connection.Todo.find({'completed': True}):
        td.delete()

    return redirect(url_for(actual_state))


@app.route('/complete', methods=['POST'])
def complete_todo():
    global actual_state
    completed = request.form['completed']

    if completed == 'True':
        completed = False
    else:
        completed = True

    connection.Todo.find_and_modify({'_id': ObjectId(request.form['id'])}, {'$set': {'completed': completed}})
    return redirect(url_for(actual_state))


@app.route('/complete_all', methods=['POST'])
def complete_all_todos():
    global actual_state
    completed = True

    if int(request.form['items_left']) == 0:
        completed = False

    for td in connection.Todo.find():
        td['completed'] = completed
        td.save()

    return redirect(url_for(actual_state))
