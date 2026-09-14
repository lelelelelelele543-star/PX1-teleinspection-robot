"""Compatibility entry point. Canonical source: current/CAD/PX1_Current_Master.py."""
from pathlib import Path
import sys,runpy
current=Path(__file__).resolve().parents[2]/"current"/"CAD"
sys.path.insert(0,str(current))
runpy.run_path(str(current/"PX1_Current_Master.py"),run_name="__main__")
