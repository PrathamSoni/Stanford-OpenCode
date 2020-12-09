import self_modify

# Currently doesn't work (see TODOs)
def example_fun():
    # Need to call function_start() at the beginning of each function.
    self_modify.function_start()

    for i in range(10):
        a = 4
        print(a)

        new_line = 'a = {}'.format(a+1)

        # Need to store and reload global variables before and after replace_line
        # Need to return False on the line after replace_line
        self_modify.user_variables['a'] = a
        self_modify.replace_line(__file__, 9, new_line, 2)
        if(self_modify.need_to_jump): return False
        a = self_modify.user_variables['a']

    new_line = 'a = {}'.format(0)
    self_modify.replace_line(__file__, 9, new_line, 2)

    # Need to return True
    return True

# Currently does work
# This function demonstrates that code edited *behind* the current line doesn't
# get re-executed, but code edited *in front of* the current line does get executed
# at the correct time.
def example_fun_noblocks():
    # Need to call function_start() at the beginning of each function.
    self_modify.function_start()

    a = 0
    print("Assigned first a")

    # Need to store and reload global variables before and after replace_line
    # Need to return False on the line after replace_line
    new_line = 'a = {}'.format(1)
    self_modify.user_variables['a'] = a
    self_modify.replace_line(__file__, 35, new_line, 1)
    if(self_modify.need_to_jump): return False
    a = self_modify.user_variables['a']

    print("Modified first line")

    new_line = 'a = {}'.format(2)
    self_modify.user_variables['a'] = a
    self_modify.replace_line(__file__, 58, new_line, 1)
    if(self_modify.need_to_jump): return False
    a = self_modify.user_variables['a']

    print("Modified second line")

    # Expected output: 0 and then 2
    print(a)
    a = 0
    print(a)

    print("Assigned second a")

    # Reset the lines

    new_line = 'a = {}'.format(0)
    self_modify.user_variables['a'] = a
    self_modify.replace_line(__file__, 35, new_line, 1)
    if(self_modify.need_to_jump): return False
    a = self_modify.user_variables['a']

    new_line = 'a = {}'.format(0)
    self_modify.user_variables['a'] = a
    self_modify.replace_line(__file__, 58, new_line, 1)
    if(self_modify.need_to_jump): return False
    a = self_modify.user_variables['a']

    return True
