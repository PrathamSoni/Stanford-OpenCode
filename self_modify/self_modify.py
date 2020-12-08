import importlib
import os
import sys


def init_globals():
    global user_module
    user_module = []

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

# Jump to a spot in the function calling *replace_line*
# Required going back multiple frames
def jump(lineno):
    frame = sys._getframe().f_back.f_back
    called_from = frame
    print(frame)

    def hook(frame, event, arg):
        if event == 'line' and frame == called_from:
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

def foo():
    # a = 1
    # j(51)
    # a = 2 #jump 2
    # print(1)
    # print(2) #jump 1
    # if a == 1:
    #     j(49)
    # print(4)
    jump(61)

foo()
