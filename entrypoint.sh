#!/bin/sh
set -e

APP_HOST=0.0.0.0
APP_PORT=${APP_PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-INFO}

SERVER_LOG_LEVEL=$(echo ${LOG_LEVEL} | tr "[:upper:]" "[:lower:]")

prod() {
  exec uvicorn \
  --factory app.main:HTTPApp.create_app \
  --host ${APP_HOST} --port ${APP_PORT} \
  --log-level ${SERVER_LOG_LEVEL} \
  --no-use-colors \
  --no-access-log
}

dev() {
  exec uvicorn --factory app.main:HTTPApp.create_app \
  --host ${APP_HOST} --port ${APP_PORT} \
  --reload
}

case "$1" in
  prod)
    shift
    prod
    ;;
  dev)
    shift
    dev
    ;;
  *)
    exec "$@"
    ;;
esac
