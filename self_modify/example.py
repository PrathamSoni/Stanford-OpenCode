import self_modify

def example_fun():
    # Need to call function_start() at the beginning of each function.
    self_modify.function_start()

    for i in range(10):
        a = 2
        print(a)

        new_line = 'a = {}'.format(a+1)

        # Need to store and reload global variables before and after replace_line
        # TODO: store a
        self_modify.replace_line(__file__, 8, new_line, 2)
        # TODO: get cached a

    new_line = 'a = {}'.format(0)
    self_modify.replace_line(__file__, 5, new_line, 2)

    # Need to return True
    return True
