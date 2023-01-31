#! /usr/bin/env pypy

import sys

if __name__ == "__main__":
    argv = sys.argv

    if len(argv) == 1:
        print("USAGE: %s <FILE>" % argv[0])
        print("[ERROR] no <FILE> is provided")
        sys.exit(1)

    source_path = argv[1]
    source_file = open(source_path, "r")

    source = source_file.read()
    source = list(source)

    source_file.close()
