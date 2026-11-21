#!/usr/bin/env python3
"""news-image-20261121 entry: copy the artwork to /output/entry.png.

The artwork is entry.png beside this file: a one-page newspaper front
page summing up Saturday 21 November 2026 in six stories (Russian
missiles land in Poland and NATO's chief heads to Warsaw, Wall Street's
AI sell-off pushes the S&P 500 into correction, COP31 runs into overtime
with fossil fuels erased from the draft, JPMorgan, Visa and Mastercard
confirm a vendor data breach, the EU disburses a record 7.9 billion
euros to Ukraine, and Nikhil Gupta is jailed for 19 years over the
Pannun murder plot). Standard library only, no network, deterministic:
the same bytes are written on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly the bytes written: refuse a partial copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy incomplete")


if __name__ == "__main__":
    main()
