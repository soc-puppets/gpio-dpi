import cffi
import logging

class SvDpi():

    def __init__(self, cffi_lib, scope):
        self._lib = cffi_lib
        self._ffi = cffi.FFI()
        if isinstance(scope, str):
            self._scopename = scope
            self._scope = self.get_scope_from_name()
        else:
            self._scope = scope
            self._scopename = self.get_name_from_scope()

    def ensure_scope(self, scope):
        if isinstance(scope, str):
            return self.get_scope_from_name(scope)
        return scope

    def get_scope_from_name(self, name=None):
        _name = name or self._scopename
        return self._lib.svGetScopeFromName(_name.encode('ascii'))

    def get_name_from_scope(self, scope=None):
        _scope = scope or self._scope
        return self._ffi.string(self._lib.svGetNameFromScope(_scope)).decode('ascii')

    def current_scope(self):
        scope = self._lib.svGetScope()
        name = self.get_name_from_scope(scope)
        return scope, name

    def set_scope(self, scope=None):
        _scope = scope or self._scope
        _scope = self.ensure_scope(_scope)
        self._lib.svSetScope(_scope)

    def __enter__(self):
        self._oldscope, _ = self.current_scope()
        self.set_scope()
        return self

    def __exit__(self, type, value, traceback):
        self.set_scope(self._oldscope)




