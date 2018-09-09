import dis
import os
import sys
from contextlib import redirect_stdout
from io import StringIO

from pyeval import my_exec

filename = sys.argv[1]

DEBUG = int(os.environ.get("DEBUG", 0))


with open(filename) as f:
    # Read and parse the .pypy file
    source = f.read()
    co_obj = compile(source, filename, mode="exec")

    if DEBUG:
        output = StringIO()
        with redirect_stdout(output):
            dis.dis(co_obj)
        print(output.getvalue())

    # Scope
    my_globals = {  # builtins
        "print": print,
        "42": 42,
        "nr12": 12,
        "jos_henken": "Ik ben Jos Henken",
    }
    my_locals = {}

    # Run bytecode
    exit_value = my_exec(co_obj, my_globals, my_locals)
