import logging
from .libpytb import ffi, lib
from gpio_dpi.gpio_dpi import GpioDpi
from gpio_dpi.svdpi import SvDpi

class PyTb():

    SEQ = [
        (0x00, 0xff),
        (0x01, 0xff),
        (0x02, 0xff),
        (0x04, 0xff),
        (0x08, 0xff),
        (0x10, 0xff),
        (0x20, 0xff),
        (0x40, 0xff),
        (0x80, 0xff),
        (0x00, 0xff)
    ]

    def __init__(self):
        _, tb_scope = SvDpi(lib, "").current_scope()
        self._gpio = GpioDpi(f"{tb_scope}.u_gpio_dpi", lib)
        self._n = 0

    def init(self):
        self._gpio.set_in(0, enables=0)

    def onclock(self):
        gpio_out = self._gpio.get_out()
        logging.info(f"gpio_out = 0x{gpio_out:02x}")

        if self._n >= len(self.SEQ):
            lib.simulator_request_finish()
        else:
            (val, en) = self.SEQ[self._n]
            self._gpio.set_in(val, enables=en)
        self._n += 1

    def shutdown(self):
        pass
