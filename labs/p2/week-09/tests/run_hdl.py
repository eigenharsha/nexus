#!/usr/bin/env python3
"""Run the nand2tetris hardware simulator over this lab's .tst scripts.

The simulator ships with the Nand2Tetris software suite:
    https://www.nand2tetris.org/software
Point NEXUS_HDL_SIM at HardwareSimulator.sh (or .bat), or put it on PATH.

Exit code 0 means every .tst script for the track produced a .out identical to its .cmp.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent

# chip name -> lowest track that requires it
CHIPS = {
    "ALU": 2,
    "Add16": 1,
    "Add16CLA": 3,
    "And": 1,
    "And16": 1,
    "Bit": 2,
    "DMux": 1,
    "DMux4Way": 1,
    "DMux8Way": 1,
    "FullAdder": 1,
    "HalfAdder": 1,
    "Inc16": 2,
    "Mux": 1,
    "Mux16": 1,
    "Mux4Way16": 1,
    "Mux8Way16": 1,
    "Not": 1,
    "Not16": 1,
    "Or": 1,
    "Or16": 1,
    "Or8Way": 1,
    "PC": 2,
    "RAM16K": 2,
    "RAM4K": 2,
    "RAM512": 2,
    "RAM64": 2,
    "RAM8": 2,
    "Register": 2,
    "Xor": 1,
}
LEVEL = {"basic": 1, "standard": 2, "hard": 3}


def find_sim() -> str | None:
    env = os.environ.get("NEXUS_HDL_SIM")
    if env and Path(env).exists():
        return env
    return shutil.which("HardwareSimulator.sh") or shutil.which("HardwareSimulator")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--impl", default="starter")
    ap.add_argument("--track", default="standard")
    args = ap.parse_args()

    impl = LAB / args.impl
    want = LEVEL[args.track]
    sim = find_sim()
    if sim is None:
        print("ERROR: the Nand2Tetris HardwareSimulator was not found.", file=sys.stderr)
        print("  Download the software suite from https://www.nand2tetris.org/software", file=sys.stderr)
        print("  then: export NEXUS_HDL_SIM=/path/to/tools/HardwareSimulator.sh", file=sys.stderr)
        return 2

    failures, ran = [], 0
    for chip, level in sorted(CHIPS.items(), key=lambda kv: (kv[1], kv[0])):
        if level > want:
            continue
        hdl = impl / f"{chip}.hdl"
        tst = HERE / "scripts" / f"{chip}.tst"
        if not tst.exists():
            failures.append(f"{chip}: no test script at {tst.relative_to(LAB)}")
            continue
        if not hdl.exists():
            failures.append(f"{chip}: {hdl.relative_to(LAB)} does not exist")
            continue
        ran += 1
        proc = subprocess.run([sim, str(tst)], capture_output=True, text=True)
        blob = (proc.stdout + proc.stderr).strip()
        if proc.returncode != 0 or "Comparison failure" in blob or "error" in blob.lower():
            failures.append(f"{chip}: {blob.splitlines()[0] if blob else 'failed'}")
        else:
            print(f"  ok      {chip}")

    for f in failures:
        print(f"  not ok  {f}", file=sys.stderr)
    print(f"\n  {ran - len(failures)} chips passed, {len(failures)} failed")
    return 1 if failures or ran == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
