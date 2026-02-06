import os
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path so `server` package imports correctly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server import safe_functions as sf


def test_simple_handle_request_false(capsys):
    sf.simple_handle_request(False)
    captured = capsys.readouterr()
    assert "Menjalankan tugas normal" in captured.out


def test_simple_handle_request_true(capsys):
    sf.simple_handle_request(True)
    captured = capsys.readouterr()
    assert "Menjalankan operasi kritis" in captured.out


def test_auth_handle_request_unauthorized(tmp_path, monkeypatch, capsys):
    logpath = tmp_path / "audit.log"
    logger = sf.setup_audit_logger(str(logpath))

    # Ensure no ADMIN_TOKEN set
    monkeypatch.delenv("ADMIN_TOKEN", raising=False)

    sf.auth_handle_request(None, logger=logger)
    captured = capsys.readouterr()
    assert "Menjalankan tugas normal" in captured.out

    content = logpath.read_text()
    assert "unauthorized_or_normal" in content


def test_auth_handle_request_wrong_token(tmp_path, monkeypatch, capsys):
    logpath = tmp_path / "audit.log"
    logger = sf.setup_audit_logger(str(logpath))

    monkeypatch.setenv("ADMIN_TOKEN", "supersecret")

    sf.auth_handle_request("wrong-token", logger=logger)
    captured = capsys.readouterr()
    assert "Menjalankan tugas normal" in captured.out
    assert "unauthorized_or_normal" in logpath.read_text()


def test_auth_handle_request_correct_token(tmp_path, monkeypatch, capsys):
    logpath = tmp_path / "audit.log"
    logger = sf.setup_audit_logger(str(logpath))

    monkeypatch.setenv("ADMIN_TOKEN", "supersecret")

    sf.auth_handle_request("supersecret", logger=logger)
    captured = capsys.readouterr()
    assert "Menjalankan operasi kritis" in captured.out
    assert "authorized_access" in logpath.read_text()
