#!/usr/bin/env bash
# Render build helper: upgrade packaging tools and install requirements
set -e
python -m pip install -U pip setuptools wheel && pip install -r requirements.txt
