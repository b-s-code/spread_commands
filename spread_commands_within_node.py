#!/usr/bin/env python3

import sys
import subprocess

def main():
    if len(sys.argv) != 4:
        print("Usage: spread_commands_within_node.py start_line end_line path/to/commands.txt")
        sys.exit(1)

    start_line = int(sys.argv[1])
    end_line = int(sys.argv[2])
    commands_file = sys.argv[3]

    with open(commands_file, 'r') as f:
        all_commands = [line.strip() for line in f if line.strip()]
    selected_commands = all_commands[start_line:end_line]

    processes = []
    for cmd in selected_commands:
        print(f"Running: {cmd}")
        processes.append(subprocess.Popen(cmd, shell=True))

    for p in processes:
        p.wait()

if __name__ == "__main__":
    main()
