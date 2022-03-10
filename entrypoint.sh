#!/bin/bash
set -e

APP_HOST=0.0.0.0
APP_PORT=${APP_PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

prod() {
  exec uvicorn app.main:HTTPApp.create_app --host ${APP_HOST} --port ${APP_PORT} \
  --log-level ${LOG_LEVEL} --no-use-colors --no-access-log --factory

}

dev() {
  exec uvicorn app.main:HTTPApp.create_app --host ${APP_HOST} --port ${APP_PORT} --reload --factory
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
