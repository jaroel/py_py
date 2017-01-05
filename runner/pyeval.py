import os
import importable_modules

_marker = []

DEBUG = int(os.environ.get('DEBUG', 0))

# byte codes
POP_TOP = 1
LOAD_NAME = 101
LOAD_CONST = 100
CALL_FUNCTION = 131
RETURN_VALUE = 83
STORE_NAME = 90
IMPORT_NAME = 108


# handlers
def handle_LOAD_NAME(co_codes, co_obj, stack, scope):
    position = co_codes.pop()
    co_codes.pop()
    name = co_obj.co_names[position]
    value = scope[name]
    DEBUG and print('LOAD_NAME', value)
    stack.append(value)


def handle_STORE_NAME(co_codes, co_obj, stack, scope):
    position = co_codes.pop()
    co_codes.pop()
    name = co_obj.co_names[position]
    value = stack.pop()
    DEBUG and print('STORE_NAME', name, value)
    scope.locals[name] = value


def handle_LOAD_CONST(co_codes, co_obj, stack, scope):
    position = co_codes.pop()
    co_codes.pop()
    value = co_obj.co_consts[position]
    DEBUG and print("LOAD_CONST", value)
    stack.append(value)


def handle_CALL_FUNCTION(co_codes, co_obj, stack, scope):
    amount_args = co_codes.pop()
    co_codes.pop()  # something with kwargs?

    args = [stack.pop() for _ in range(amount_args)]
    kwargs = {}  # ignore kwargs for now

    func = stack.pop()

    # Call the Python level function.
    # The Python interpreter would call a C function
    DEBUG and print("CALL_FUNCTION", func, args, kwargs)
    return_val = func(*args, **kwargs)

    stack.append(return_val)


def handle_POP_TOP(co_codes, co_obj, stack, scope):
    stack.pop()


def handle_RETURN_VALUE(co_codes, co_obj, stack, scope):
    value = stack.pop()
    DEBUG and print("RETURN_VALUE", value)
    return value


def handle_IMPORT_NAME(co_codes, co_obj, stack, scope):
    co_codes.pop()  # ?
    co_codes.pop()  # ?
    stack.pop()  # None return val

    name = co_obj.co_names[0]
    module = getattr(importable_modules, name, _marker)
    if module is _marker:
        raise ImportError('cannot import ' + name + ' from importable_modules')

    stack.append(module)


handlers = {
    LOAD_NAME: handle_LOAD_NAME,
    STORE_NAME: handle_STORE_NAME,
    LOAD_CONST: handle_LOAD_CONST,
    CALL_FUNCTION: handle_CALL_FUNCTION,
    POP_TOP: handle_POP_TOP,
    RETURN_VALUE: handle_RETURN_VALUE,
    IMPORT_NAME: handle_IMPORT_NAME,
}


class Scope:
    def __init__(self, my_globals, my_locals):
        self.globals = my_globals
        self.locals = my_locals

    def __getitem__(self, name):
        if name in self.locals:
            return self.locals[name]
        elif name in self.globals:
            return self.globals[name]
        else:
            raise NameError(name)


def my_exec(co_obj, my_globals, my_locals):
    co_codes = list(reversed(co_obj.co_code))
    stack = []
    scope = Scope(my_globals, my_locals)

    while co_codes:
        DEBUG == 2 and print("co_codes: \n", co_codes)
        b_code = co_codes.pop()
        handler = handlers[b_code]
        return_val = handler(co_codes, co_obj, stack, scope)
    return return_val
