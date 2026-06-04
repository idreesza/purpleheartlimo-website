#!/bin/bash
set -e

# Static single-file site (index.html) served by python3 server.py.
# No dependencies to install, no build step, no migrations.
# Kept as a no-op so task merges reconcile workflows cleanly.

echo "post-merge: static site, nothing to build."
