#!/usr/bin/env python3

import os
import sys
import math

CORES_PER_NODE = 4  # Example core count for testing
SBATCH_TEMPLATE = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks={ntasks}
#SBATCH --cpus-per-task=1
#SBATCH --job-name=spread_cmds_node_{node_id}
#SBATCH --output=spread_cmds_node_{node_id}.out

srun python3 spread_commands_within_node.py {start_line} {end_line} {commands_file}
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: spread_commands path/to/commands.txt")
        sys.exit(1)

    commands_file = sys.argv[1]

    with open(commands_file, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]
    total_commands = len(commands)

    num_nodes = math.ceil(total_commands / CORES_PER_NODE)

    for node_id in range(num_nodes):
        start_line = node_id * CORES_PER_NODE
        end_line = min((node_id + 1) * CORES_PER_NODE, total_commands)

        sbatch_script = SBATCH_TEMPLATE.format(
            ntasks=end_line - start_line,
            node_id=node_id,
            start_line=start_line,
            end_line=end_line,
            commands_file=commands_file
        )

        script_filename = f"spread_node_{node_id}.sbatch"
        with open(script_filename, 'w') as f:
            f.write(sbatch_script)

        print(f"Generated: {script_filename}")

if __name__ == "__main__":
    main()
