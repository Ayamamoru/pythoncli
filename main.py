import argparse
import sys
import os
import json
from datetime import datetime

TASKS_FILE = "tasks.json"
VERSION = "1.2.0"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def format_task(task):
    status = "><>" if not task ["done"] else "[x]"
    priority = task.get("priority", "medium")
    priority_labels = {"low": "(low)", "medium": "(med)", "high": "(!!!)"}
    label = priority_labels.get(priority, "(med)")
    due = f"  -- due: {task['due']}" if task.get("due") else ""
    return f"{status} {label} {task['id']}: {task['task']}{due}"

parser = argparse.ArgumentParser(
    prog="fishk"
    description="fishk -- a fishy little task manager",
)

parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION} ~o>><>")
parser.add_argument("task", type=str, nargs="?", help="task to reel in!")
parser.add_argument("-l", "--list", action="store_true", help="show yo whole catch")
parser.add_argument("-c", "--catch", type=int, metavar="ID", help="mark a task as caught (complete)")

