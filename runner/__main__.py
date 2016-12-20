import os
import dis
import sys
from io import StringIO
from contextlib import redirect_stdout
from pyeval import my_exec

filename = sys.argv[1]

DEBUG = int(os.environ.get('DEBUG', 0))


def make_42():
    return 42


class Kekjo:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


with open(filename) as f:
    # Read and parse the .pypy file
    source = f.read()
    co_obj = compile(source, filename, mode='exec')

    if DEBUG:
        output = StringIO()
        with redirect_stdout(output):
            dis.dis(co_obj)
        print(output.getvalue())

    # Scope
    my_globals = {
        'print': print,
        'make_42': make_42,
        '42': 42,
        'nr12': 12,
        'jos_henken': Kekjo('Ik ben Jos Henken'),
    }
    my_locals = {}

    # Run bytecode
    exit_value = my_exec(co_obj, my_globals, my_locals)
