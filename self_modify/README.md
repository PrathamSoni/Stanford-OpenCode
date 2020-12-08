# Self-Modify
## A Simple Library for Self-Modifying python

**Usage:**

```
import self_modify

def example_fun():
    # Need to call function_start() at the beginning of each function.
    self_modify.function_start()

    for i in range(10):
        a = 0
        print(a)

        new_line = 'a = {}'.format(a+1)

        # Need to store and reload global variables before and after replace_line
        # Need to return False on the line after replace_line
        # TODO: store a
        self_modify.replace_line(__file__, 8, new_line, 2)
        return False
        # TODO: get cached a

    # new_line = 'a = {}'.format(0)
    # self_modify.replace_line(__file__, 8, new_line, 2)

    # Need to return True
    return True
```

**Design:**

Python can easily reload functions after they have been modified, and the changed will take effect the next time the function is called. The tricky bit is that we have to make the function _appear_ to continue running from where the `replace_line` function was called. This is done with some `sys` black magic. Here's how:

1. `replace_line` replaces the line, sets a flag indicating that the file has been edited, stores the line it was called from, and then the caller returns `False`.
2. `run.py` then calls the user's function again. This time `function_start` uses debugger hooks to jump directly to the line saved by `replace_line`. (TODO: This is broken right now)

Users are currently required to cache global variables themselves manually.

**TODOs:**

**Jumping to a line in a different file does not work right now.**

It would be nice to have `replace_line` force its parent function to return `False` rather than having the user add that line.

It would be nice to have `replace_line` cache the user's variables for them, rather than the user having to do that manually.

It would be nice for `function_start` to not be necessary.
