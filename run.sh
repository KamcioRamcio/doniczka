#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

DB_MODULE="database.database"
FLASK_MODULE="flask_app.app"
LCD_MODULE="hardware.lcd_display"

setsid python -m "$DB_MODULE" &
DB_PID=$!
echo "DB session PID: $DB_PID"

setsid python -m "$FLASK_MODULE" &
FLASK_PID=$!
echo "Flask session PID: $FLASK_PID"

setsid python -m "$LCD_MODULE" &
LCD_PID=$!
echo "LCD session PID: $LCD_PID"



cleanup() {
  echo "Shutting down processes..."
  kill -INT -"${DB_PID}" 2>/dev/null || true
  kill -INT -"${FLASK_PID}" 2>/dev/null || true
  kill -INT -"${LCD_PID}" 2>/dev/null || true

  sleep 1
  kill -TERM -"${DB_PID}" 2>/dev/null || true
  kill -TERM -"${FLASK_PID}" 2>/dev/null || true
  kill -TERM -"${LCD_PID}" 2>/dev/null || true

  wait "${DB_PID}" 2>/dev/null || true
  wait "${FLASK_PID}" 2>/dev/null || true
  wait "${LCD_PID}" 2>/dev/null || true
}

trap 'cleanup; exit' SIGINT SIGTERM

wait -n
exit_code=$?
cleanup
exit $exit_code
