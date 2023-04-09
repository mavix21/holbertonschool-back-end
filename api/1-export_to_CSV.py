#!/usr/bin/python3
"""This module gathers data from an API"""
import csv
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

    user_requested = next((user for user in users
                           if str(user.get("id")) == employee_id), None)

    if not user_requested:
        print("The employee with id {} does not exist".format(employee_id))
        exit(1)

    employee_username = user_requested.get("username")

    all_tasks = [todo for todo in todos
                 if str(todo.get("userId")) == employee_id]

    # Export to CSV region
    filename = f"{employee_id}.csv"
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for task in all_tasks:
            task_completed_status = task.get("completed")
            task_title = task.get("title")
            writer.writerow([
                employee_id,
                employee_username,
                task_completed_status,
                task_title])
