from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from night_clerk.pipeline import run_packet_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="night-clerk")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Process one inbox packet and write a receipt")
    run.add_argument("--packet", required=True, help="Path to inbox JSON packet")
    args = parser.parse_args(argv)

    if args.cmd == "run":
        receipt = run_packet_file(Path(args.packet))
        json.dump(receipt.model_dump(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
