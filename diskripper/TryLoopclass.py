from LogOrNotclass import LogOrNot
import time

class TryLoop(LogOrNot):
    """TryLoop class for handling exceptions in a try-except block.
    Example usage:
    tl = tl()
    tl.tl(func, *args, **kwargs)
    """
    def __init__(self, log_mode='terminal', log_file_path='try_loop.log'):
        LogOrNot.__init__(self, log_mode=log_mode, log_file_path=log_file_path)
        self.log_debug("TryLoop class initialized")
        
    def tl(self, func, *args, **kwargs): #Depreciate this function in favor of  class decorators
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.log_error(f"Error: {e}")
            return None
    
    @staticmethod    
    def debug_func(self, func):
        def wrapper():
            t1 = time.time()
            self.log_debug(f"Executing {func.__name__}")
            func()
            t2 = time.time()-t1
            self.log_debug(f"Executed {func.__name__} in {t2} seconds")
        return wrapper
    
    @staticmethod
    def try_func(func):
        def wrapper(*args, **kwargs):
            log_instance = LogOrNot()
            try:
                t1 = time.time()
                log_instance.log_debug(f"Executing {func.__qualname__}")
                t2 = time.time()-t1
                log_instance.log_debug(f"Executed {func.__qualname__} in {t2} seconds")
                return func(*args, **kwargs)
            except Exception as e:
                log_instance.log_error(f"Error: {e}")
                return None
        return wrapper