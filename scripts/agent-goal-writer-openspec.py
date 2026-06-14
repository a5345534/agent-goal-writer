#!/usr/bin/env python3
"""Compatibility wrapper for the renamed goal-spec OpenSpec helper."""
from pathlib import Path
import os
import sys

helper = Path(__file__).resolve().with_name("goal-spec-openspec.py")
os.execv(sys.executable, [sys.executable, str(helper), *sys.argv[1:]])
