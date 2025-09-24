# spread_commands

Run a list of single process commands across more CPU cores than one HPC node provides.

## User story

As a HPC workflow developer, I want an easy way to distribute a list of commands across multiple nodes, so that:

- I can run a list of commands in parallel,
- where the list is longer than the number of CPU cores on one node,
- and each command can run using only a single core,
- without having to write code to perform this operation for each new workflow.

## Limitations

Because spread_commands is optimised to minimise wall time, it is cost-inefficient for cases where the memory used per process is much less than a node's memory per CPU core.

The processes run by each command are not explicity bound to specific CPU cores.

No --time value is set in SBATCH directive so a default value will be used.

## Interface

`spread_commands path/to/commands.txt`

## Implementation

User calls `spread_commands path/to/commands.txt`.

`spread_commands` is a Python script that:

1. Makes an assumption about the number of CPU cores per node on the current HPC system (hardcoded.)
2. Determines the number of commands in commands.txt (number of lines minus number of empty lines).
3. Generates a number of slurm batch scripts; one per node that will be requested.  Each slurm batch script:

    1. hardcodes which line numbers in commands.txt correspond to commands that should be run by *that node*,
    2. calls `srun` on another Python script `spread_commands_within_node`, passing along the relevant line numbers and the path to `commands.txt`.

`spread_commands_within_node` is a Python script which runs once on each work node.  It:

1. does not need to know number of CPU cores per node
2. is not called directly by the user,
3. reads `commands.txt` and saves to its memory just those commands which correspond to those line numbers,
4. starts a subprocess for each relevant command, and then,
5. exits once all subprocesses have completed.
