from datetime import datetime
from api.database import get_connection


def create_task(title, description, priority, due_date):
    # insert a new task and return the created row
    conn = get_connection()
    now = datetime.now().isoformat()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO tasks (title, description, priority, created_date, due_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, description, priority, now, due_date),
    )
    conn.commit()

    task_id = cur.lastrowid
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()
    task = dict(row) if row else {"id": task_id}

    conn.close()
    return task


def get_tasks(status=None, priority=None):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if status:
        sql += " AND status=?"
        params.append(status)
    if priority:
        sql += " AND priority=?"
        params.append(priority)

    cur.execute(sql, params)
    rows = cur.fetchall()
    tasks = [dict(r) for r in rows]
    conn.close()
    return tasks


def update_task(task_id, title=None, description=None, priority=None, due_date=None):
    conn = get_connection()
    cur = conn.cursor()

    # check exists
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    if not cur.fetchone():
        conn.close()
        return {"error": "Task not found"}

    parts = {}
    if title is not None:
        parts["title"] = title
    if description is not None:
        parts["description"] = description
    if priority is not None:
        parts["priority"] = priority
    if due_date is not None:
        parts["due_date"] = due_date

    if not parts:
        conn.close()
        return {"message": "No changes"}

    set_clause = ", ".join([f"{k}=?" for k in parts.keys()])
    values = list(parts.values())
    values.append(task_id)

    cur.execute(f"UPDATE tasks SET {set_clause} WHERE id=?", values)
    conn.commit()

    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    updated = dict(cur.fetchone())
    conn.close()
    return {"message": "Task updated", "task": updated}


def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted"}


def mark_complete(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    row = cur.fetchone()
    task = dict(row) if row else {"id": task_id}
    conn.close()
    return {"message": "Task completed", "task": task}
