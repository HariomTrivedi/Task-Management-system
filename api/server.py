from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

from api.database import init_db
from api.task_manager import (
    create_task,
    get_tasks,
    delete_task,
    mark_complete,
    update_task,
)


class TaskAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/tasks":
            query = urllib.parse.parse_qs(parsed.query)
            status = query.get("status", [None])[0]
            priority = query.get("priority", [None])[0]

            tasks = get_tasks(status, priority)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(tasks).encode())

    def do_POST(self):

        # create task
        if self.path == "/tasks":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except (TypeError, ValueError):
                content_length = 0

            if content_length == 0:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty request body"}).encode())
                return

            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                return

            if not data.get("title"):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "'title' is required"}).encode())
                return

            task = create_task(
                data["title"],
                data.get("description"),
                data.get("priority", "medium"),
                data.get("due_date"),
            )

            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(task).encode())
            return

        # mark complete via POST /tasks/{id}/complete
        if self.path.startswith("/tasks/") and self.path.endswith("/complete"):
            parts = self.path.strip("/").split("/")
            if len(parts) >= 2:
                try:
                    task_id = int(parts[1])
                except ValueError:
                    self.send_response(400)
                    self.end_headers()
                    return

                result = mark_complete(task_id)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                return

    def do_PATCH(self):
        # update task via PATCH /tasks/{id}
        if self.path.startswith("/tasks/"):
            try:
                task_id = int(self.path.split("/")[-1])
            except ValueError:
                self.send_response(400)
                self.end_headers()
                return

            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except (TypeError, ValueError):
                content_length = 0

            if content_length == 0:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty request body"}).encode())
                return

            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                return

            result = update_task(
                task_id,
                data.get("title"),
                data.get("description"),
                data.get("priority"),
                data.get("due_date"),
            )

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            return

    def do_DELETE(self):

        if self.path.startswith("/tasks/"):

            task_id = int(self.path.split("/")[-1])

            result = delete_task(task_id)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())


def run():

    init_db()

    server = HTTPServer(("localhost", 8000), TaskAPI)

    print("Server running on http://localhost:8000")

    server.serve_forever()


if __name__ == "__main__":
    run()
