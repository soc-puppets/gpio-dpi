#!/usr/bin/env python3

import cffi

################################################################################
# Configuration
################################################################################

libname = "libpytb"

ffibuilder = cffi.FFI()

################################################################################
# Embedding API
#
# These are the C declarations of the functions we want the server to provide,
# (i.e. DPI imports in the simulator), and then their (Python) implementations.
################################################################################

typedefs = """
    typedef void* svScope;
"""

# C prototypes of DPI imports

ffibuilder.embedding_api(f"""
    {typedefs}

    // DPI imports - implemented here, called by simulator

    int pytb_init(void);
    int pytb_onclock(void);
    int pytb_shutdown(void);

""")

# Embedding API function implementations

ffibuilder.embedding_init_code("""
    import logging

    from libpytb import ffi
    from pytb.pytb import PyTb

    tb = PyTb()

    # If the init code fails entirely, functions will return 0, so use +ve
    # values to indicate success.
    @ffi.def_extern(error=-1)
    def pytb_init():
        tb.init()
        return 1

    @ffi.def_extern(error=-1)
    def pytb_onclock():
        tb.onclock();
        return 1

    @ffi.def_extern(error=-1)
    def pytb_shutdown():
        tb.shutdown()
        return 1

""")

################################################################################
# Foreign function interface.
#
# These are declarations of C functions that we want to be able to call from our
# Python code.
# They might be:
# - DPI exports from SV
# - svdpi functions (e.g. svSetScope())
# - anything from any other library we link
#
# Note that these declarations could be parsed from one or more header files, if
# such files were to exist.
#
# After we've called this build script, other python code can call these
# functions by doing e.g.
#
#   from .libpytb import lib
#   lib.simulator_request_finish()
################################################################################

external_functions = """
    // DPI exports - implemented in SV, called here

    extern void simulator_request_finish(void);

    extern unsigned int gpio_get_out(void);
    extern unsigned int gpio_get_in(void);
    extern unsigned int gpio_get_in_oe(void);

    extern void gpio_set_in   (unsigned int value);
    extern void gpio_set_in_oe(unsigned int value);

    // Implemented by the simulator itself

    extern svScope svGetScope();
    extern svScope svSetScope(const svScope scope);

    extern const char* svGetNameFromScope(const svScope);
    extern svScope svGetScopeFromName(const char* scopeName);
"""

ffibuilder.set_source(libname, f"""
    {typedefs}
    {external_functions}
    """,
    libraries=['c'],
)

ffibuilder.cdef(external_functions)

################################################################################
# Compile
################################################################################

ffibuilder.compile(target=f"{libname}.so", verbose=True)
