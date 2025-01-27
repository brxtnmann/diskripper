from EzSQL import *
from OSclass import *
from TryLoopclass import *
from drive_utils import *
import ffmpeg
import time
import threading


def open_cache_n_batch(output_loc: str, profile):
    size: int = 0
    media: list[str] = []
    paths: list[str] = []
    buffer: int = 1_000_000_000
    
    cachemap: list[tuple[int,str,str,int]] = db.cachemap.fetch_all()
    for tple in cachemap:
        size.__add__(tple[3])
        media.append(tple[1])
        paths.append(tple[2])
    
    
    if PathOperations(output_loc).get_dir_size() >= size-buffer:
        for i, path in enumerate(paths):
            output_loc = output_loc + '/' + media[i] + '/' + media[i]
            print(f'Transcoding {media[i]} from {path} and outputting at {output_loc}')
            transcode_n_concat(path, output_loc, profile)
            print(f'Moving on')
    else:
        LogOrNot.log_error('Output location is too small')
        
def transcode_n_concat(mount: str, output_loc: str, profile: str) -> None:
    
    profile_data = db.profiles.fetch_one('profile', profile)
    dskf = diskfinder(mount)
    vid = dskf.dvdvidext.upper #add logic for different disk types
    input_file, *_, = dskf.getmedia()
    input_files = []
    for file in input_file:   
        if file.upper().endswith(f'.{vid}'):
            input_files.append(file)
        else:
            pass
    input_files_str = '|'.join(input_files)
    
    ffmpeg.input(f'concat:{input_files_str}') \
        .output(f'{output_loc}{profile_data[0]}.mp4', #I may need to add a / or \ before output_
                acodec=profile_data[1], 
                b=profile_data[2], 
                format=profile_data[3], 
                vf=f'scale={profile_data[4]}') \
        .run()
        
        
def main(output_loc: str = 'Z:/Movies', mount: str = 'S:/'):
    global db
    db = EzSQLiteDB(f'{output_loc}/diskripper.db')
    open_cache_n_batch(output_loc, "fhd")
    
if __name__ == '__main__':
    main()