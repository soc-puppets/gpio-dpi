# gpio-dpi
GPIO testbench agent, controlled via DPI

This is intended to be an easily-reused component, but for now it serves as an
example of integrating SV and Python via DPI-C and CFFI.

## Running the Testbench

Requires verilator 5.x

```
cd testbench/run
source sourceme
make build
./obj_dir/Vtb
```

The sourceme creates a Python virtual env with the appropriate dependencies, and
sets up $PYTHONPATH.
