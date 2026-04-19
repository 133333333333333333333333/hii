#!/usr/bin/env bash
exec gunicorn app:app --bind 0.0.0.0:${PORT:-5001}
