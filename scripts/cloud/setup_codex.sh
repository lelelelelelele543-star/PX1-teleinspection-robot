#!/usr/bin/env bash
# Run as the environment setup command for PX1 Codex Cloud (Ubuntu/Debian).
set -Eeuo pipefail
python3 -m pip install --upgrade pip
python3 -m pip install 'cadquery>=2.6,<3'
python3 -c 'import cadquery; print("CadQuery OK", cadquery.__version__)'
if ! command -v FreeCADCmd >/dev/null 2>&1 && ! command -v freecadcmd >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y freecad xvfb
  else
    echo "FreeCAD not found; install it for the Codex cloud environment" >&2
    exit 2
  fi
fi
echo "PX1 CAD dependencies prepared."
echo "The main master uses CadQuery; FreeCAD is provided for inspecting the resulting STEP."
echo "Run: bash scripts/cloud/build_current.sh"
