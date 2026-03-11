import argparse
import json
import sys

import requests

API_BASE = "http://localhost:8000"


# simple JSON pretty-print
def _p(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def list_tasks(status=None, priority=None):
    # fetch list from API
    params = {}
    if status:
        params["status"] = status
    if priority:
        params["priority"] = priority

    r = requests.get(API_BASE + "/tasks", params=params)
    r.raise_for_status()
    _p(r.json())


def create_task_cli(title, description=None, priority="medium", due_date=None):
    payload = {"title": title, "priority": priority}
    if description:
        payload["description"] = description
    if due_date:
        payload["due_date"] = due_date

    r = requests.post(API_BASE + "/tasks", json=payload)
    r.raise_for_status()
    _p(r.json())


def update_task_cli(task_id, title=None, description=None, priority=None, due_date=None):
    payload = {}
    if title:
        payload["title"] = title
    if description:
        payload["description"] = description
    if priority:
        payload["priority"] = priority
    if due_date:
        payload["due_date"] = due_date

    if not payload:
        print("Nothing to update")
        return

    r = requests.patch(f"{API_BASE}/tasks/{task_id}", json=payload)
    r.raise_for_status()
    _p(r.json())


def complete_task_cli(task_id):
    r = requests.post(f"{API_BASE}/tasks/{task_id}/complete")
    r.raise_for_status()
    _p(r.json())


def delete_task_cli(task_id):
    r = requests.delete(f"{API_BASE}/tasks/{task_id}")
    r.raise_for_status()
    _p(r.json())


def main(argv=None):
    parser = argparse.ArgumentParser(prog="task-cli", description="Task Manager CLI")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("list", help="List tasks")
    p.add_argument("--status", choices=["pending", "completed"], help="Filter by status")
    p.add_argument("--priority", choices=["low", "medium", "high"], help="Filter by priority")

    p = sub.add_parser("create", help="Create a task")
    p.add_argument("title", help="Task title")
    p.add_argument("--description", help="Task description")
    p.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    p.add_argument("--due_date", help="Due date YYYY-MM-DD")

    p = sub.add_parser("update", help="Update a task")
    p.add_argument("id", type=int, help="Task id")
    p.add_argument("--title", help="New title")
    p.add_argument("--description", help="New description")
    p.add_argument("--priority", choices=["low", "medium", "high"], help="New priority")
    p.add_argument("--due_date", help="New due date YYYY-MM-DD")

    p = sub.add_parser("complete", help="Mark complete")
    p.add_argument("id", type=int, help="Task id")

    p = sub.add_parser("delete", help="Delete a task")
    p.add_argument("id", type=int, help="Task id")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "list":
            list_tasks(args.status, args.priority)
        elif args.cmd == "create":
            create_task_cli(args.title, args.description, args.priority, args.due_date)
        elif args.cmd == "update":
            update_task_cli(args.id, args.title, args.description, args.priority, args.due_date)
        elif args.cmd == "complete":
            complete_task_cli(args.id)
        elif args.cmd == "delete":
            delete_task_cli(args.id)
        else:
            parser.print_help()
    except requests.RequestException as e:
        print("Request failed:", str(e))
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(e.response.json())
            except Exception:
                print(e.response.text)
        sys.exit(1)


if __name__ == '__main__':
    main()
