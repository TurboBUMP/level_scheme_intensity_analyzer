import functools
import time

################################################################################
################################ DECORATORS ####################################

def timer(function):
    @functools.wraps(function)
    def wrapper_timer(*args,**kwargs):
        start_time=time.time()
        result=function(*args,**kwargs)
        stop_time=time.time()
        print('*'*80)
        print(f'\t{function.__name__} took {stop_time-start_time:3f}s')
        print('*'*80)
        return result
    return wrapper_timer

################################ DECORATORS ####################################
################################################################################
