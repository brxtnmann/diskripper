import logging
import inspect

class LogOrNot:
    def __init__(self, log_mode='terminal', log_file_path=None):
        self.logger = logging.getLogger('LogOrNot')
        self.logger.setLevel(logging.DEBUG)
        
        if log_mode == 'terminal':
            handler = logging.StreamHandler()
        elif log_mode == 'file' and log_file_path:
            handler = logging.FileHandler(log_file_path)
        elif log_mode == 'none':
            handler = logging.NullHandler()
        else:
            raise ValueError("Invalid log_mode or missing log_file_path for file logging")
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_error(self, message):
        callers = self.contextofactive()
        self.logger.error(f'{message} called by {callers}')
        
    def log_info(self, message):
        self.logger.info(message)
        
    def set_level(level):
        log = logging.getLogger('LogOrNot')
        level = level.upper()
        if level == 'DEBUG':
            log.setLevel(logging.DEBUG)
        elif level == 'INFO':
            log.setLevel(logging.INFO)
        elif level == 'WARNING':
            log.setLevel(logging.WARNING)
        elif level == 'ERROR':
            log.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            log.setLevel(logging.CRITICAL)
        else:
            raise ValueError(f"Invalid logging level: {level}")
        
    def callersofactive(self):
        try:
            frames = inspect.stack()
            callers = []
            for i in range(2, len(frames)):
                callers.append(frames[i][3])
            return ">".join(callers)
        except IndexError:
            pass
        
    def contextofactive(self):
        try:
            frames = inspect.stack()
            callers = []
            for i in range(2, len(frames)):
                callers.append(''.join(frames[i][4]))
            return ">".join(callers)
        except IndexError:
            pass        
    
        
    def log_debug(self = None, message = None):
        if isinstance(self, str) and message == None:
            message = self
            logging.debug(message)            
        else:
            try:
                callers = self.callersofactive()
                self.logger.debug(f'{message} called by {callers}')
            except:
                pass
        
        

# Example usage:
# logger = LogOrNot(log_mode='file', log_file_path='/path/to/logfile.log')
# logger.log_error('This is an error message')