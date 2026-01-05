#!/usr/bin/env python3
"""
Safe, "almost real" tools for prototype scripts.

These tools are intentionally limited:
  - No shell execution
  - DB is an in-memory SQLite database with synthetic demo data
  - File ops are constrained to allowed directories (defaults to /tmp)
"""

from __future__ import annotations

import ast
import json
import os
import sqlite3
import tempfile
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Union


class ToolExecutionError(RuntimeError):
    pass


Number = Union[int, float]


def _is_subpath(candidate: str, allowed_dir: str) -> bool:
    candidate_abs = os.path.abspath(os.path.expanduser(candidate))
    allowed_abs = os.path.abspath(os.path.expanduser(allowed_dir))
    allowed_prefix = allowed_abs.rstrip(os.sep) + os.sep
    return candidate_abs == allowed_abs or candidate_abs.startswith(allowed_prefix)


def _validate_path(path: str, allowed_dirs: Iterable[str]) -> str:
    expanded = os.path.abspath(os.path.expanduser(path))
    for allowed_dir in allowed_dirs:
        if _is_subpath(expanded, allowed_dir):
            return expanded
    raise ToolExecutionError(
        f"Path {path!r} is not under allowed dirs: {', '.join(allowed_dirs)}"
    )


class _SafeArithmetic(ast.NodeVisitor):
    _allowed_binops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
    _allowed_unaryops = (ast.UAdd, ast.USub)

    def visit(self, node: ast.AST) -> Number:
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, self._allowed_unaryops):
            return +self.visit(node.operand) if isinstance(node.op, ast.UAdd) else -self.visit(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, self._allowed_binops):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self._apply(node.op, left, right)
        raise ToolExecutionError("Unsupported expression")

    @staticmethod
    def _apply(op: ast.operator, left: Number, right: Number) -> Number:
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.Pow):
            return left ** right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.FloorDiv):
            return left // right
        raise ToolExecutionError("Unsupported operator")


def calculator(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval")
        result = _SafeArithmetic().visit(tree)
        return str(result)
    except ToolExecutionError:
        raise
    except Exception as exc:
        raise ToolExecutionError(f"Failed to evaluate expression: {exc}") from exc


def web_search(query: str) -> str:
    query_lower = query.lower()
    if "opentelemetry" in query_lower:
        results = [
            {"title": "OpenTelemetry", "url": "https://opentelemetry.io/", "snippet": "Observability framework."},
            {"title": "OTel Semantic Conventions", "url": "https://opentelemetry.io/docs/specs/semconv/", "snippet": "Standard attributes and spans."},
        ]
    else:
        results = [
            {"title": "Example result", "url": "https://example.com/", "snippet": f"Results for: {query}"},
        ]
    return json.dumps({"query": query, "results": results}, indent=2)


def _init_demo_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE products (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          price_usd REAL NOT NULL
        );
        INSERT INTO products (name, price_usd) VALUES
          ('Widget', 9.99),
          ('Gadget', 14.50),
          ('Doodad', 3.25);

        CREATE TABLE categories (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL
        );
        INSERT INTO categories (name) VALUES
          ('Tools'),
          ('Accessories');

        CREATE TABLE public_info (
          id INTEGER PRIMARY KEY,
          info TEXT NOT NULL
        );
        INSERT INTO public_info (info) VALUES
          ('This is synthetic demo data.'),
          ('No real customer data is stored.');

        CREATE TABLE users (
          id INTEGER PRIMARY KEY,
          email TEXT NOT NULL
        );
        INSERT INTO users (email) VALUES
          ('user1@example.com'),
          ('user2@example.com');
        """
    )
    conn.commit()


def database_query(conn: sqlite3.Connection, query: str) -> str:
    stripped = query.strip().rstrip(";")
    if not stripped.lower().startswith("select"):
        raise ToolExecutionError("Only SELECT queries are allowed in the demo database")
    if ";" in stripped:
        raise ToolExecutionError("Multiple statements are not allowed")

    cur = conn.cursor()
    try:
        cur.execute(stripped)
        columns = [d[0] for d in cur.description] if cur.description else []
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        return json.dumps({"query": stripped, "rows": rows}, indent=2)
    except sqlite3.Error as exc:
        raise ToolExecutionError(f"Database error: {exc}") from exc


@dataclass
class DemoToolExecutor:
    allowed_read_dirs: List[str]
    allowed_write_dirs: List[str]
    _db: sqlite3.Connection
    _outbox_dir: str

    @classmethod
    def create_default(cls) -> "DemoToolExecutor":
        tmp = tempfile.gettempdir()
        tmp_dirs = sorted({tmp, "/tmp"})
        outbox_dir = os.path.join(tmp, "genai-security-guardian-outbox")
        os.makedirs(outbox_dir, exist_ok=True)

        db = sqlite3.connect(":memory:")
        _init_demo_db(db)

        return cls(
            allowed_read_dirs=tmp_dirs,
            allowed_write_dirs=tmp_dirs,
            _db=db,
            _outbox_dir=outbox_dir,
        )

    def execute(self, tool_name: str, args: Dict[str, Any]) -> str:
        if tool_name == "calculator":
            return calculator(str(args.get("expression", "")))

        if tool_name in {"web_search", "search"}:
            return web_search(str(args.get("query", "")))

        if tool_name == "get_weather":
            location = str(args.get("location", "Seattle"))
            return json.dumps({"location": location, "forecast": "55°F, light rain"}, indent=2)

        if tool_name == "database_query":
            return database_query(self._db, str(args.get("query", "")))

        if tool_name == "file_read":
            path = _validate_path(str(args.get("path", "")), self.allowed_read_dirs)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()

        if tool_name in {"file_write", "write_file"}:
            path = _validate_path(str(args.get("path", "")), self.allowed_write_dirs)
            content = str(args.get("content", ""))
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return json.dumps({"path": path, "bytes_written": len(content.encode("utf-8"))}, indent=2)

        if tool_name in {"send_email", "email_send"}:
            to_addr = str(args.get("to", "recipient@example.com"))
            subject = str(args.get("subject", "Demo email"))
            body = str(args.get("body", ""))
            message_id = f"msg_{int(time.time() * 1000)}"
            path = os.path.join(self._outbox_dir, f"{message_id}.json")
            payload = {"to": to_addr, "subject": subject, "body": body, "message_id": message_id}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            return json.dumps({"status": "queued", "message_id": message_id, "outbox_path": path}, indent=2)

        if tool_name in {"read_email", "email_read"}:
            folder = str(args.get("folder", "inbox"))
            messages: List[Dict[str, Any]] = []
            try:
                for entry in sorted(os.listdir(self._outbox_dir)):
                    if not entry.endswith(".json"):
                        continue
                    path = os.path.join(self._outbox_dir, entry)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            messages.append(json.load(f))
                    except Exception:
                        continue
            except FileNotFoundError:
                pass

            return json.dumps({"folder": folder, "messages": messages}, indent=2)

        raise ToolExecutionError(f"Tool not supported in demo executor: {tool_name!r}")
