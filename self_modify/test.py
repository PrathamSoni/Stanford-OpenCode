import self_modify

# This file is just for testing

def test():
    print("test")
    self_modify.jump_encapulate(9)
    print("test 2")
    print("test 3")

    return True


def test_2():
    self_modify.function_start()

    print("test")

    self_modify.need_to_jump = True
    self_modify.line_called = 23
    if(self_modify.need_to_jump): return False

    print("test 2")

    return True
