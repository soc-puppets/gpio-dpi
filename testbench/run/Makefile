
PYDIR = $(abspath ../python/pytb)
$(info $(PYDIR))

$(PYDIR)/libpytb.so: $(PYDIR)/cffi_build.py
	cd $(PYDIR) && ./cffi_build.py

LDFLAGS = \
  -lpytb \
  -L$(PYDIR) \
  -Wl,-rpath,$(PYDIR)

build: $(PYDIR)/libpytb.so
	verilator --binary --timescale 1ns/1ps \
          --trace-fst \
          --top tb \
          ../../src/sv/gpio_dpi.sv \
          ../sv/tb.sv \
          -Wno-style \
          -Wno-WIDTHEXPAND \
          -Wno-WIDTHTRUNC \
          $(addprefix -LDFLAGS ,$(LDFLAGS))

