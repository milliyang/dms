#!/bin/bash
# Start DMS service
# If WAIT_FOR_INFLUXDB is set, wait for InfluxDB before starting

set -e

if [ "${WAIT_FOR_INFLUXDB:-true}" = "true" ]; then
    # Wait for InfluxDB if specified
    INFLUXDB_HOST="${INFLUXDB_HOST:-influxdb}"
    INFLUXDB_PORT="${INFLUXDB_PORT:-8086}"
    /wait-for-influxdb.sh "$INFLUXDB_HOST" "$INFLUXDB_PORT" gunicorn \
        --bind 0.0.0.0:11183 \
        --worker-class sync \
        --workers 4 \
        --timeout 30 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        app:app
else
    # Start directly without waiting
    exec gunicorn \
        --bind 0.0.0.0:11183 \
        --worker-class sync \
        --workers 4 \
        --timeout 30 \
        --log-level info \
        --access-logfile - \
        --error-logfile - \
        app:app
fi
