#!/bin/bash

export README_MD="$(cat README.md)"

env
set -e

cmd="main:app --app-dir src --host 0.0.0.0 --port 8080 --reload --reload-dir src/ --reload-dir etc/ --reload-include *.json"

# Add API root path if present
if [ ! -z "$API_ROOT_PATH" ]; then
  cmd+=" --root-path $API_ROOT_PATH"
fi

echo $cmd

eval uvicorn $cmd