"""scheduler.py
Simple cron-like task scheduler using SQLite storage.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Optional

DB_DIR = "db"
SCHED_DB = os.path.join(DB_DIR, "tasks.db")


@dataclass
class ScheduledTask:
    id: int
    command: str
    run_at: float
    repeat: bool
    retries: int = 0


class TaskScheduler(threading.Thread):
    """Background scheduler that executes tasks from SQLite."""

    def __init__(self, poll_interval: int = 60):
        super().__init__(daemon=True)
        self.poll_interval = poll_interval
        self.conn = sqlite3.connect(SCHED_DB, check_same_thread=False)
        self._create_table()
        self._stop_flag = threading.Event()

    def _create_table(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                run_at REAL NOT NULL,
                repeat INTEGER NOT NULL,
                retries INTEGER DEFAULT 0
            )
            """
        )
        self.conn.commit()

    def add_task(self, command: str, run_at: datetime, repeat: bool = False) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (command, run_at, repeat) VALUES (?, ?, ?)",
            (command, run_at.timestamp(), int(repeat)),
        )
        self.conn.commit()

    def run(self) -> None:
        while not self._stop_flag.is_set():
            self._check_tasks()
            time.sleep(self.poll_interval)

    def stop(self) -> None:
        self._stop_flag.set()

    def _check_tasks(self) -> None:
        cur = self.conn.cursor()
        now_ts = time.time()
        rows = cur.execute(
            "SELECT id, command, run_at, repeat, retries FROM tasks WHERE run_at <= ?",
            (now_ts,),
        ).fetchall()
        for id_, cmd, ts, rep, retries in rows:
            self._execute_task(id_, cmd, rep, retries)

    def _execute_task(self, task_id: int, cmd: str, repeat: int, retries: int) -> None:
        try:
            subprocess.run(cmd, shell=True, check=True)
            self._finish_task(task_id, bool(repeat))
        except subprocess.CalledProcessError:
            retries += 1
            self.conn.execute(
                "UPDATE tasks SET retries = ? WHERE id = ?", (retries, task_id)
            )
            self.conn.commit()

    def _finish_task(self, task_id: int, repeat: bool) -> None:
        if repeat:
            next_time = datetime.now().timestamp() + 86400
            self.conn.execute(
                "UPDATE tasks SET run_at = ? WHERE id = ?", (next_time, task_id)
            )
        else:
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

