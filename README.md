# py_py
Running small parts of the Python3 bytecode in Python3 itself

python3 -m venv .
# And run:  
python3 runner runme.py
# Or, for seening the opcodes and some 'C-level' vars:
DEBUG=1 python3 runner runme.py
