import importlib
import os
import sys
import inspect

def init_globals():
    global user_module
    user_module = []

    global user_variables
    user_variables = {}

    global line_called
    line_called = 0

    global need_to_jump
    need_to_jump = False

# Replace a line in the calling file
def replace_line(file, line, string, indent):

    module_name = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r') as f:
        lines = f.read().split('\n')
        spaces = "    "*indent
        new_file = '\n'.join(lines[0:line-1]+[spaces + string] + lines[line:])

    with open(file, 'w') as f:
        f.write(new_file)

    global user_module
    importlib.reload(user_module)

    caller = inspect.getframeinfo(inspect.stack()[1][0])
    global line_called
    line_called = caller.lineno

    #TODO: Make the *calling function* return False after this

# Jump to a spot in the function calling function_start
# Requires going back multiple frames
def jump(lineno):
    frame = sys._getframe().f_back.f_back
    called_from = frame
    print(frame)

    def hook(frame, event, arg):
        if True:#event == 'line' and frame == called_from:
            try:
                frame.f_lineno = lineno
            except ValueError as e:
                print("jump failed:", e)
            while frame:
                frame.f_trace = None
                frame = frame.f_back
            return None
        return hook

    while frame:
        frame.f_trace = hook
        frame = frame.f_back
    sys.settrace(hook)

# Functions using replacement need to call this function at the start
# This jumps to the line where replace_line was called
def function_start():
    global need_to_jump
    global line_called
    if(need_to_jump):
        jump(line_called)

# Testing fucntion
def jump_encapulate(line):
    jump(line)

# jump_encapulate(75)
# print(1)
# print(2)
