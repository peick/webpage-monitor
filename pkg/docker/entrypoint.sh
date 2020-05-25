#!/bin/bash
set -e

case "${1}" in
    wpmon-collector)
        shift
        exec /opt/webpage-monitor/bin/wpmon-collector "$@"
        ;;
    wpmon-pgwriter)
        shift
        exec /opt/webpage-monitor/bin/wpmon-pgwriter "$@"
        ;;
    *)
        exec "$@"
        ;;
esac
