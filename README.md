# Task Manager

This project is a simple **Task Management system** built as part of a Python developer practical assessment.

It provides a small **REST API** for managing tasks and a **command-line interface (CLI)** to interact with that API from the terminal.

The goal of the project is to demonstrate clean Python code, basic API design, and simple data persistence using **SQLite**.

The system allows you to:

* Create, update, delete, and view tasks
* Mark tasks as completed
* Filter tasks by status or priority
* Manage tasks directly from the command line

---

# Project Structure

```
task_manager/
│
├── api/
│   ├── server.py        # HTTP server exposing the REST API
│   ├── task_manager.py  # Business logic for task operations
│   └── database.py      # SQLite database connection and initialization
│
├── cli/
│   └── cli.py           # Command line interface for interacting with the API
│
├── data/
│   └── tasks.db         # SQLite database file
│
├── requirements.txt
└── README.md
```

---

# Setup Instructions

### Requirements

* Python **3.8 or higher**

---

### 1. Create a virtual environment

From the project root directory:

Windows (PowerShell or CMD):

```
python -m venv .venv
.\.venv\Scripts\activate
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Start the API server

```
python -m api.server
```

You should see:

```
Server running on http://localhost:8000
```

The API will now be available locally.

---

# API Endpoints

Base URL:

```
http://localhost:8000
```

### Get all tasks

```
GET /tasks
```

Optional filters:

```
GET /tasks?status=pending
GET /tasks?priority=high
GET /tasks?status=pending&priority=high
```

---

### Create a task

```
POST /tasks
```

Example request body:

```json
{
  "title": "Buy groceries",
  "description": "Milk and eggs",
  "priority": "high",
  "due_date": "2026-03-20"
}
```

---

### Update a task

```
PATCH /tasks/{id}
```

Only include fields you want to change.

Example:

```json
{
  "title": "Buy groceries and bread"
}
```

---

### Mark a task as completed

```
POST /tasks/{id}/complete
```

---

### Delete a task

```
DELETE /tasks/{id}
```

---

# Using the CLI

The CLI provides an easy way to interact with the API from the terminal.

Run commands from the project root directory.

---

### List tasks

```
python -m cli.cli list
```

Filter tasks:

```
python -m cli.cli list --status pending
```

---

### Create a task

```
python -m cli.cli create "Buy groceries" --description "Milk and eggs" --priority high --due_date 2026-03-20
```

---

### Update a task

```
python -m cli.cli update 1 --title "Buy bread"
```

---

### Mark task complete

```
python -m cli.cli complete 1
```

---

### Delete a task

```
python -m cli.cli delete 1
```

---

# Code Style

The code follows **PEP 8 guidelines** and uses **Black** for formatting.

To format the project:

```
python -m black .
```

---

# Features Implemented

* REST API for task management
* Create, read, update, and delete tasks
* Mark tasks as completed
* Filter tasks by status and priority
* Command line interface for interacting with the system
* SQLite database for persistent storage

---

# Assumptions

* The API server runs locally on `localhost:8000`.
* The SQLite database file is stored in the `data/` directory.
* The CLI communicates with the API and assumes the server is already running.

---