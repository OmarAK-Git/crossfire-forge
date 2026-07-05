# Packets

The autopilot controller writes per-task implementation and verification packets here only for the loop setup task itself.

Queue tasks should use their own `item.run_dir` and keep packets under that task directory.
