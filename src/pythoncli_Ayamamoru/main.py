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
    status = "><>" if not task["done"] else "[x]"
    priority = task.get("priority", "medium")
    priority_labels = {"low": "(low)", "medium": "(med)", "high": "(!!)"}
    label = priority_labels.get(priority, "(med)")
    due = f"  -- due: {task['due']}" if task.get("due") else ""
    return f"{status} {label} {task['id']}: {task['task']}{due}"


def main():
    parser = argparse.ArgumentParser(
        prog="fishk",
        description="fishk -- a fishy little task manager",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION} ~o>><>")
    parser.add_argument("task", type=str, nargs="?", help="fish to reel in!")
    parser.add_argument("-l", "--list", action="store_true", help="show yo whole catch")
    parser.add_argument("-c", "--catch", type=int, metavar="ID", help="mark a fish as caught (complete)")
    parser.add_argument("-r", "--release", type=int, metavar="ID", help="throw a fish back (mark incomplete)")
    parser.add_argument("-d", "--drown", type=int, metavar="ID", help="delete a task by ID")
    parser.add_argument("-e", "--edit", type=int, metavar="ID", help="re-bait a task (edit text) by ID")
    parser.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Priority: low, medium, high (default: medium)",
    )
    parser.add_argument("--due", type=str, metavar="YYYY-MM-DD", help="deadline 4 task")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.due:
        try:
            datetime.strptime(args.due, "%Y-%m-%d")
        except ValueError:
            print("Error: --due must be in YYYY-MM-DD format (e.g. 2025-12-31)", file=sys.stderr)
            sys.exit(1)

    if args.list:
        tasks = load_tasks()
        if not tasks:
            print("~~ the waters are empty... cast a line! ~~")
            print('    add a task: fishk "your task here"')
        else:
            print("~" * 42)
            print("  ><> fishk -- catch of the day")
            print("~" * 42)
            for task in tasks:
                print(f"  {format_task(task)}")
            print("~" * 42)
            total = len(tasks)
            done = sum(1 for t in tasks if t["done"])
            print(f"  {done}/{total} fish caught")

    elif args.catch is not None:
        tasks = load_tasks()
        task = find_task(tasks, args.catch)
        if task:
            task["done"] = True
            save_tasks(tasks)
            print(f"got one! task {args.catch} reeled in.")
        else:
            print(f"Error: no fish found with ID {args.catch}", file=sys.stderr)
            sys.exit(1)

    elif args.release is not None:
        tasks = load_tasks()
        task = find_task(tasks, args.release)
        if task:
            task["done"] = False
            save_tasks(tasks)
            print(f"task {args.release} thrown back into the sea.")
        else:
            print(f"Error: no fish found with ID {args.release}", file=sys.stderr)
            sys.exit(1)

    elif args.drown is not None:
        tasks = load_tasks()
        original_count = len(tasks)
        tasks = [t for t in tasks if t["id"] != args.drown]
        if len(tasks) < original_count:
            save_tasks(tasks)
            print(f"task {args.drown} swallowed by the depths.")
        else:
            print(f"Error: no fish found with ID {args.drown}", file=sys.stderr)
            sys.exit(1)

    elif args.edit is not None:
        if not args.task:
            print('Error: re-baiting requires new task text: fishk -e ID "new text"', file=sys.stderr)
            sys.exit(1)
        tasks = load_tasks()
        task = find_task(tasks, args.edit)
        if task:
            old_text = task["task"]
            task["task"] = args.task
            task["priority"] = args.priority
            if args.due:
                task["due"] = args.due
            save_tasks(tasks)
            print(f'task {args.edit} re-baited: "{old_text}" -> "{args.task}"')
        else:
            print(f"Error: no fish found with ID {args.edit}", file=sys.stderr)
            sys.exit(1)

    elif args.task:
        tasks = load_tasks()
        new_id = tasks[-1]["id"] + 1 if tasks else 1
        new_task = {
            "id": new_id,
            "task": args.task,
            "done": False,
            "priority": args.priority,
        }
        if args.due:
            new_task["due"] = args.due
        tasks.append(new_task)
        save_tasks(tasks)
        priority_labels = {"low": "(low)", "medium": "(med)", "high": "(!!)"}
        label = priority_labels.get(args.priority, "(med)")
        print(f"new fish on the line! {label} \"{args.task}\" added with ID {new_id}")


# guys i love fish
if __name__ == "__main__":
    main()
