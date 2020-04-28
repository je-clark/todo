###
# Todo list application using only exceptions and errors for flow control
###

import argparse, json, sys
from datetime import datetime

def initiate():
    description = "Manage all your TODOs with this overcomplicated application!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('todo_path', help="File path to the todo file you want to interact with.")

    args = parser.parse_args()
    return args.todo_path

def read_todo_file(file_path):
    try:
        with open(file_path) as todo_file:
            todo = json.load(todo_file)
    except json.JSONDecodeError:
        # We don't want to corrupt a file that is in the wrong format.
        print(f"{file_path} exists, but is not a valid JSON file. Exiting")
        sys.exit()
    except:
        # If the file doesn't exist, then we create a new file
        print(f"{file_path} does not exist, starting a new todo list.")
        todo = {}
    finally:
        return todo

def user_interface(todo, file_path):
    
    user_input = input("> ")

    try:
        try:
            assert "show" == user_input.lower()
            show(todo, file_path)
        except AssertionError:
            pass
        try:
            assert "show closed" == user_input.lower()
            show_closed(todo, file_path)
        except AssertionError:
            pass
        try:
            cmd = "show task "
            assert cmd in user_input.lower()
            show_task(todo, user_input.lower().replace(cmd,''), file_path)
        except AssertionError:
            pass
        try:
            cmd = "add notes "
            assert cmd in user_input.lower()
            add_notes(todo, user_input.lower().replace(cmd,''), file_path)
        except AssertionError:
            pass
        try:
            cmd = "add subtask "
            assert cmd in user_input.lower()
            add_subtask(todo,user_input.lower().replace(cmd,''), file_path)
        except AssertionError:
            pass
        try:
            cmd = "add "
            assert cmd in user_input.lower()
            add_task(todo, user_input.lower().replace(cmd,''), file_path)
        except AssertionError:
            pass
        try:
            cmd = "close "
            assert cmd in user_input.lower()
            close_task(todo, user_input.lower().replace(cmd,''), file_path)
        except AssertionError:
            pass
        try:
            assert "exit" == user_input.lower()
            exit(todo, file_path)
        except AssertionError:
            pass
        try:
            assert "help" == user_input.lower()
            help(todo, file_path)
        except AssertionError:
            pass
        raise SyntaxError
    except SyntaxError:
        print("Syntax Error")
        user_interface(todo, file_path)



def show(todo, file_path):
    for task in todo.keys():
        try:
            complete = todo[task]["completed_timestamp"]
        except KeyError:
            print(task)

    user_interface(todo, file_path)

def show_closed(todo, file_path):
    for task in todo.keys():
        try:
            complete = todo[task]["completed_timestamp"]
        except KeyError:
            continue  
        else:
            print(task)          
            
    user_interface(todo, file_path)

def show_task(todo, task_name, file_path):
    try:
        task = todo[task_name]
        try:
            print(f"Task Notes:\n    {task['notes']}")
        except KeyError:
            pass
        try:
            subtasks = task['subtasks']
            print("Subtasks:")
            for sub in subtasks:
                print(f"    {sub['name']}")
        except KeyError:
            pass
        try:
            print(f"This task was completed at {task['completed_timestamp']}")
        except KeyError:
            pass
    except KeyError:
        print("No task found")
    
    user_interface(todo, file_path)

def add_task(todo, task_name, file_path):
    todo[task_name] = {}

    user_interface(todo, file_path)

def add_notes(todo, task_name, file_path):
    note = input(f"Enter note for {task_name}: ")
    try:
        todo[task_name]["notes"] = note
    except KeyError:
        print("No task found")

    user_interface(todo, file_path)

def add_subtask(todo, task_name, file_path):
    subtask = input(f"Enter subtask for {task_name}: ")
    try:
        todo[task_name]["subtasks"].append({"name": subtask})
    except KeyError:
        try:
            task = todo[task_name]
        except KeyError:
            print("No task found")
        else:
            todo[task_name]["subtasks"] = [{"name": subtask}]

    user_interface(todo, file_path)

def close_task(todo, task_name, file_path):
    try:
        complete = todo[task_name]["completed_timestamp"]
        raise ValueError
    except ValueError:
        # Ironicaly, the error is that there is a value
        print("Task already closed. Nothing else to do")
    except KeyError:
        try:
            task = todo[task_name]
            todo[task_name]["completed_timestamp"] = str(datetime.now())
        except KeyError:
            print("No task found")

    user_interface(todo, file_path)

def exit(todo, file_path):
    with open(file_path, 'w') as todo_file:
        json.dump(todo, todo_file)

    sys.exit()
    

def help(todo, file_path):
    help_text = '''Help text for the todo application:

    To see an overview of all open tasks, type "show"
    To see an overview of all closed tasks, type "show closed"
    To see details of a task, type "show task {task name}"
    To create a new task, type "add {task name}"
    To add notes to a task, type "add notes {task name}"
    To add a subtask to a task, type "add subtask {task name}"
    To close a task, type "close {task name}"
    To save your changes and exit the program, type "exit"

    To display this message, type "help"

    '''
    print(help_text)
    user_interface(todo, file_path)



todo_file_path = initiate()
todo = read_todo_file(todo_file_path)
user_interface(todo, todo_file_path)