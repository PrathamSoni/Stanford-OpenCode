import importlib
import sys
import os
import self_modify
import shelve

# Usage: python run.py example.py example_fun
if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print("run.py takes in two inputs, the file to run and the function to run")
    else:
        # TODO: Handle arbitrary locations for files
        # TODO: Handle Windows style paths
        input_file = sys.argv[1]
        module_name = os.path.splitext(input_file)[0]
        input_func = sys.argv[2]

        # Make self_modify.py import the input file
        import_string = "import " + module_name
        self_modify.replace_line("self_modify.py", 5, import_string, 0, is_self = True)
        importlib.reload(self_modify)

        # import the input file ourselves and call the function
        user_module = importlib.import_module(module_name)
        function_to_call = getattr(user_module, input_func)
        function_to_call()
