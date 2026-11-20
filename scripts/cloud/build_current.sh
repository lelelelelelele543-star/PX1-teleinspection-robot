#!/usr/bin/env bash
# Rebuild the current integrated master with CadQuery in an isolated output tree.
set -Eeuo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="${PX1_CLOUD_OUT:-${REPO}/_cloud_build}"
PYTHON="${PYTHON:-python3}"

if [[ "$OUT" == "$REPO/current" || "$OUT" == "$REPO" ]]; then
  echo "Refusing to overwrite tracked source tree" >&2
  exit 2
fi
mkdir -p "$OUT/CAD/vendor" "$OUT/logs"
cp "$REPO/current/CAD/PX1_Current_Master.py" "$OUT/CAD/PX1_Current_Master.py"
cp "$REPO/current/CAD/release_tools.py" "$OUT/CAD/release_tools.py"
cp "$REPO/current/HOLD_REGISTER.json" "$OUT/HOLD_REGISTER.json"
rm -rf "$OUT/CAD/vendor_py"; cp -r "$REPO/current/CAD/vendor_py" "$OUT/CAD/vendor_py"
for vendor in Pololu_25D_75_99_Manufacturer.step Pololu_G2_24v13_Manufacturer.step WeAct_F4_64Pin_V11_Manufacturer.step; do
  test -s "$REPO/current/CAD/vendor/$vendor" || { echo "Missing vendor model: $vendor" >&2; exit 3; }
  cp "$REPO/current/CAD/vendor/$vendor" "$OUT/CAD/vendor/$vendor"
done

"$PYTHON" -c 'import cadquery; print("CadQuery", cadquery.__version__)' | tee "$OUT/logs/environment.log"
export PX1_OUT="$OUT"
# Keep the full collision results; never hide errors or promote HOLD to PASS.
"$PYTHON" "$OUT/CAD/PX1_Current_Master.py" 2>&1 | tee "$OUT/logs/build.log"
"$PYTHON" "$REPO/scripts/cloud/report.py" "$OUT"
echo "PX1 cloud CAD build: $OUT"
