import os
import subprocess
import time
from datetime import datetime

import pytest

import scheduler


def test_add_task_persists(monkeypatch, scheduler_db):
    monkeypatch.setattr(scheduler, "SCHED_DB", scheduler_db)
    sched = scheduler.TaskScheduler(poll_interval=0.01)
    sched.add_task("echo hi", datetime.fromtimestamp(time.time()))
    cur = sched.conn.cursor()
    cur.execute("SELECT command FROM tasks")
    assert cur.fetchone()[0] == "echo hi"


def test_execute_task_success(monkeypatch, scheduler_db):
    monkeypatch.setattr(scheduler, "SCHED_DB", scheduler_db)
    sched = scheduler.TaskScheduler(poll_interval=0.01)
    called = []
    def fake_run(cmd, shell=True, check=True):
        called.append(cmd)
    monkeypatch.setattr(subprocess, "run", fake_run)
    sched.add_task("echo hi", datetime.fromtimestamp(time.time()))
    sched._check_tasks()
    assert called == ["echo hi"]
