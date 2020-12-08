import importlib
import os

# Below import is sacrificial for run.py
import example

def replace_line(file, line, string, indent, is_self = False):

    module_name = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r') as f:
        lines = f.read().split('\n')
        spaces = "    "*indent
        new_file = '\n'.join(lines[0:line-1]+[spaces + string] + lines[line:])

    with open(file, 'w') as f:
        f.write(new_file)

    if not is_self:
        user_module = importlib.import_module(module_name)
        importlib.reload(user_module)
