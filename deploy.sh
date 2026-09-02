#!/usr/bin/env bash
# deploy.sh
set -euo pipefail
HOST=dymco99@192.168.1.105
DEST=/home/dymco99/Documents/programs/robotic-arm

rsync -az --delete \
  --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
  --exclude '*.xlsx' --exclude 'mechanical_design' \
  ./ "$HOST:$DEST/"

ssh -tX "$HOST" "cd $DEST && python3 -m venv --system-site-packages .venv 2>/dev/null; .venv/bin/pip install -r requirements.txt && .venv/bin/python src/test_stepper.py $*"
