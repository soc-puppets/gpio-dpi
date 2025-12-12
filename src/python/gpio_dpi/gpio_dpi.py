import logging
from .svdpi import SvDpi

class GpioDpi():

    def __init__(self, scopename, cffi_lib):
        self._svdpi = SvDpi(cffi_lib, scopename)
        self._lib = cffi_lib

    def set_in(self, value, enables=None):
        with self._svdpi:
            self._lib.gpio_set_in(value)
            if enables is not None:
                self._lib.gpio_set_in_oe(enables)

    def get_out(self):
        with self._svdpi:
            out = self._lib.gpio_get_out()
        return out

