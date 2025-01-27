import os
import shutil
from LogOrNotclass import LogOrNot

class LoggingOperations:
    Mode = 'file'
    LogPath = 'file_ops.log'
    logger = LogOrNot(log_mode=Mode, log_file_path=LogPath)
    
    @classmethod
    def change_log_location(cls, new_log_path):
        cls.logger.log_error(f"Changing log file location to {new_log_path}")
        cls.LogPath = new_log_path
        cls.logger = LogOrNot(log_mode=cls.Mode, log_file_path=cls.LogPath)
        cls.logger.log_error(f"Log file location changed to {new_log_path}")
        
    @classmethod
    def change_log_mode(cls, new_mode): 
        cls.logger.log_error(f"Changing log mode to {new_mode}")
        cls.Mode = new_mode
        cls.logger = LogOrNot(log_mode=cls.Mode, log_file_path=cls.LogPath)
        cls.logger.log_error(f"Log mode changed to {new_mode}")
        
        """Example usage:
        foobar = {any_class_func_in_script}()
        foobar.change_log_location('new_log_file.log')
        foobar.change_log_mode('terminal')     
        """

class systemOperations(LoggingOperations):
    def __init__(self):
        super().__init__()
        
    def get_os(self) -> str:
        return os.name
        
class FileOperations(LoggingOperations):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, 'r') as file:
            return file.read()

    def write_file(self, content):
        with open(self.file_path, 'w') as file:
            file.write(content)

    def append_file(self, content):
        with open(self.file_path, 'a') as file:
            file.write(content)

class DirectoryOperations(LoggingOperations):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def create_directory(self):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
            self.logger.log_info(f"Directory created: {self.dir_path}")
        else:
            self.logger.log_info(f"Directory already exists: {self.dir_path}")

    def delete_directory(self):
        if os.path.exists(self.dir_path):
            shutil.rmtree(self.dir_path)
            self.logger.log_info(f"Directory deleted: {self.dir_path}")
        else:
            self.logger.log_info(f"Directory not found: {self.dir_path}")

    @staticmethod
    def change_working_directory(new_dir):
        os.chdir(new_dir)

    @staticmethod
    def execute_command(command):
        return os.system(command)

class PathOperations(LoggingOperations):
    def __init__(self, start_path):
        self.start_path = start_path

    def walk_directory(self):
        for dirpath, dirnames, filenames in os.walk(self.start_path):
            yield dirpath, dirnames, filenames

    def find_all_files(self):
        all_files = []
        for dirpath, _, filenames in os.walk(self.start_path):
            for filename in filenames:
                all_files.append(os.path.join(dirpath, filename))
        return all_files
    
    def find_files_by_extension(self, extension: str, *args: str) -> list[str]:
        files = []
        #add handling for extension arg getting passed as a set
        if not extension.startswith('.'):
            ".".join(extension)
        else:
            pass
        extensions = [extension, extension.upper()]
        if args:
            for arg in args:
                if not arg.startswith('.'):
                    ".".join(arg)
                else:
                    pass
                extensions.append(arg)
                extensions.append(arg.upper())
        else:
            pass
        for dirpath, _, filenames in os.walk(self.start_path):
            for filename in filenames:
                for ext in extensions:
                    if filename.endswith(f'{ext}'):
                        files.append(os.path.join(dirpath, filename))
        return files
    
    def copy_files_by_extension(self, dest_dir: str, ext: str, *args:str) -> None:
        files = self.find_files_by_extension(ext, *args)
        for file in files:
            try:
                shutil.copy(file, os.path.join(dest_dir, os.path.basename(file)))
                self.logger.log_info(f"Moved {file} to {dest_dir}")
            except FileNotFoundError:
                self.logger.log_info(f"File not found: {file}")
    
    def move_files_by_extension(self, extension, dest_dir):
        files = self.find_files_by_extension(extension)
        for file in files:
            try:
                shutil.move(file, os.path.join(dest_dir, os.path.basename(file)))
                self.logger.log_info(f"Moved {file} to {dest_dir}")
            except FileNotFoundError:
                self.logger.log_info(f"File not found: {file}")
                
    def get_dir_size(self, path: str = None) -> int:
        if not path: path = self.start_path
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size