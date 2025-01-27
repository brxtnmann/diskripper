from OSclass import *
from EzSQL import *

all_dirs = []
all_files = []
vob_files = []

class diskfinder():
    def __init__(self, mount: str):
        self.mount = mount
        self.dvdvidext = 'vob'
        self.dvdinfoext = 'ifo'
        self.dvdbupext = 'bup'
        self.blurayexts = []
        self.cdexts = []
    
    def getdsk(self, type: str, mount: str = None) -> str:
        pathtodsk = None
        if type == 'dvd' or 'DVD':
            pathidentifier = 'VIDEO_TS'
        else:
            raise NotImplementedError()
        for path, dirnames, file in os.walk(mount):     
            if dirnames:
                all_dirs.append([path, dirnames])
            if path.endswith(pathidentifier):
                pathtodsk = path
                return pathtodsk
            else:
                pathtodsk = 'did not work'
        return pathtodsk
    
    def getmedia(self, type: str = 'dvd', mount: str = None) -> tuple[list[str], str, str]:
        if self.mount and not mount: mount = self.mount
        else: LogOrNot.log_error('mount location not found')
        pathtodsk = self.getdsk(type, mount)
        association = pathtodsk.split('\\')
        diskname = str(association[-2])
        pathops = PathOperations(mount)
        if type == 'dvd' or 'DVD': files = pathops.find_files_by_extension(self.dvdvidext, self.dvdinfoext, self.dvdbupext)
        elif type == 'bd' or 'BD' or 'Bluray' or 'bluray': files = pathops.find_files_by_extension(self.blurayexts)
        elif type == 'cd' or 'CD': files = pathops.find_files_by_extension(self.cdexts)
        else:
            raise NotImplementedError('I need to build the ext list in the init function')
        return files, diskname, pathtodsk

class diskcacher(diskfinder):
    def __init__(self, mount: str, cache_location: str = './'):
        super().__init__(mount)
        self.cache_loc = cache_location
        
        
    def cache_media(self, type: str = 'dvd') -> None:
        self.pathtodsk = pathtodsk = self.getdsk(type, self.mount)
        association = pathtodsk.split('\\')
        self.diskname = diskname = association[-2]
        DirectoryOperations(diskname).change_working_directory(self.cache_loc)
        DirectoryOperations(diskname).create_directory()
        self.cachedir = cachedir = ''.join([self.cache_loc, '/', diskname])
        pathops = PathOperations(pathtodsk)
        if type == 'dvd' or 'DVD': pathops.copy_files_by_extension(cachedir, self.dvdvidext, self.dvdinfoext, self.dvdbupext)
        elif type == 'bd' or 'BD' or 'Bluray' or 'bluray': pathops.copy_files_by_extension(cachedir, self.blurayexts)
        elif type == 'cd' or 'CD': pathops.copy_files_by_extension(cachedir, self.cdexts)
        else:
            raise NotImplementedError('I need to build the ext list in the init function')
        return None