import importlib
import os
import globals

def replace_line(file, line, string, indent):

    module_name = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r') as f:
        lines = f.read().split('\n')
        spaces = "    "*indent
        new_file = '\n'.join(lines[0:line-1]+[spaces + string] + lines[line:])

    with open(file, 'w') as f:
        f.write(new_file)

    importlib.reload(globals.user_module)
