#!/usr/bin/python3
"""This module gathers data from an API"""
import requests
from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: {argv[0]} employee_id")
        exit(1)

    employee_id = argv[1]

    response_todos = requests.get("https://jsonplaceholder.typicode.com/todos")
    response_users = requests.get("https://jsonplaceholder.typicode.com/users")

    # Check if the requests were successful (status code 200)
    if response_todos.status_code != 200 or response_users.status_code != 200:
        print("Failed to fetch data.")
        print("TODOS response status code: {:d}".format(response_todos))
        print("Users response status code: {:d}".format(response_users))
        exit(1)

    todos = response_todos.json()
    users = response_users.json()

    user_requested = None
    for user in users:
        if user.get("id") and str(user.get("id")) == employee_id:
            user_requested = user
            break

    if not user_requested:
        print("The employee with id {} does not exist".format(employee_id))
        exit(1)

    employee_name = user_requested.get("name")
    all_tasks = [todo for todo in todos
                 if str(todo.get("userId")) == employee_id]
    total_number_of_tasks = len(all_tasks)

    completed_tasks = [todo for todo in all_tasks
                       if todo.get("completed") is True]
    number_of_done_tasks = len(completed_tasks)

    print(f"Employee {employee_name} is done with tasks \
{number_of_done_tasks}/{total_number_of_tasks}:")

    for task in completed_tasks:
        print("\t {}".format(task.get("title")))
