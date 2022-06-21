#!/bin/bash
set -e

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <url>"
  exit 1
fi

data='{
  "status": "firing",
  "startsAt": "2018-01-01T00:00:00Z",
  "endsAt": "",
  "labels": {
    "alertname": "TestAlert",
    "instance": "test-instance",
    "job": "test-job",
    "service": "test-service",
    "severity": "critical"
  },
  "annotations": {
    "description": "Test Alert",
    "summary": "Test Alert"
  },
  "generatorURL": "https://google.com"
}'
url=$1

curl -X POST -H "Content-Type: application/json" -d "$data" "$url"

