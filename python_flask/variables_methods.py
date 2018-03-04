import functools

def my_decorator(func):
    @functools.wraps(func)
    def function_that_runs_funs():
        print("I'm the decorator")
        func()
    return function_that_runs_funs

@my_decorator
def my_function():
    print("i'm the function")


my_function()
