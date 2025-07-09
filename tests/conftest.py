import os
import json
import os
import json
import sys
from datetime import datetime

import pytest

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from auth_rbac import AuthManager, Role


@pytest.fixture()
def temp_auth_db(tmp_path):
    return str(tmp_path / "auth.db")


@pytest.fixture()
def auth_manager(temp_auth_db):
    return AuthManager(db_path=temp_auth_db)


@pytest.fixture()
def sample_commands_json(tmp_path):
    data = {
        "test.echo": {
            "phrases": ["echo message"],
            "params": {"msg": {"type": "string", "required": True}},
            "templates": {"win": "echo {msg}", "astro": "echo {msg}"}
        }
    }
    file_path = tmp_path / "commands.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return str(file_path)


@pytest.fixture()
def scheduler_db(tmp_path):
    return str(tmp_path / "tasks.db")
