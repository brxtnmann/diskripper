from EzSQL import *
from OSclass import *
from TryLoopclass import *
from drive_utils import *
import ffmpeg
import time
import threading

db = None

@TryLoop.try_func
def prompt_for_profile() -> str:
    try:
        profiles = db.profiles.fetch_column('profile')
    except:
        pass      
    if not profiles:
        db.profiles.create('profile -txt -pk, audio_codec -txt, bitrate -int, output_format -txt, resolution -txt, gui -txt, error_handling -txt, user_input -txt')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"sd", "copy", "128000", "libx264", "360p30", "n", "y", "0"')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"540p", "copy", "128000", "libx264", "540p30", "n", "y", "0"')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"hd", "copy", "128000", "libx264", "720p30", "n", "y", "0"')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"fhd", "copy", "128000", "libx264", "1080p30", "n", "y", "0"')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"1440p", "copy", "128000", "libx264", "1440p30", "n", "y", "0"')
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input', '"uhd", "copy", "128000", "libx264", "2160p30", "n", "y", "0"')
        profiles: list[tuple[str]] = db.profiles.fetch_column('profile')
    else:
        pass
    
    print('Available profiles:')
    for i, profile in enumerate(profiles, start = 1):
        print(f"{i}.{profile}")
    print(f'{len(profiles) + 1}. Add profile: *** WARNING YOU MUST USE ACCEPTED INPUT TYPES, THERE ARE NO GRUARD RAILS ***')
    
    choice = input(f'Pick a profile: (1-{len(profiles).__add__(1)})').strip()
    if choice.isdigit() and 1 <= int(choice) <= len(profiles):
        profile, *_ = profiles[int(choice) - 1]
        return str(profile)
    elif choice == str(len(profiles) + 1):
        inputs = [input(prompt) for prompt in [
            'Input profile name:', 
            'Input audio codec type:', 
            'Input chosen bitrate:', 
            'Input desired output format:', 
            'Input desired resolution:', 
            'Input gui toggle(y/n):', 
            'Input error handling toggle (y/n):', 
            'Input user input toggle (1/0):'
        ]]
        db.profiles.insert('profile, audio_codec, bitrate, output_format, resolution, gui, error_handling, user_input',f'"{inputs[0]}", "{inputs[1]}", "{inputs[2]}", "{inputs[3]}", "{inputs[4]}", "{inputs[5]}", "{inputs[6]}", "{inputs[7]}"')
        return str(inputs[0])
    else:
        pass

def cache_and_map(mount: str, cache: str = None) -> None:
    db.cachemap.create('id -int -pk -ai, media_name -txt, path -txt, size -int')
    os.system('devmon -u')
    os.system('devmon -a')
    time.sleep(30)
    cacher = diskcacher(mount, cache)
    cacher.cache_media()
    media_name = cacher.diskname
    cachepath = cacher.cachedir
    osc = PathOperations(cachepath)
    dirsize = osc.get_dir_size()
    db.cachemap.insert('media_name, path, size', f'"{media_name}", "{cachepath}", {dirsize}')
    
def transcode_n_concat(mount: str, output_loc: str, profile) -> None:
    
    profile_data: tuple[str,str,str,int,str,str,str,str,str] = db.profiles.fetch_one('profiles', f'profile="{profile}"')
    dskf = diskfinder(mount)
    vid = dskf.dvdvidext.upper #add logic for different disk types
    input_file, *_, = dskf.getmedia()
    input_files = []
    for file in input_file:
        if file.upper.endswith(f'.{vid}'):
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
        for path, name in paths and media:
            output_loc = output_loc + '/' + name + '/' + name
            LogOrNot.log_info(f'Transcoding {name} from {path} and outputting at {output_loc}')
            transcode_n_concat(path, output_loc, profile)
            LogOrNot.log_info(f'Moving on')
    else:
        LogOrNot.log_error('Output location is too small')
    

def cache_and_map_with_retry(mount: str, cache: str = None) -> None:
    while True:
        try:
            cache_and_map(mount, cache)
            break
        except Exception as e:
            print(f"Error: {e}. Retrying in 60 seconds...")
            time.sleep(60)

def main(output_loc: str = '/Media/Jellyfin/Movies', mount: str = '/media/'): 
    global db
    db = EzSQLiteDB(f'{output_loc}/diskripper.db')
    try:
        toggle = db.userchoices.fetch_all()
    except:
        pass
    
    if not toggle:
        db.userchoices.create('profile -txt -pk, prompts -int')
        profile = prompt_for_profile()
        
        db.userchoices.insert('profile, prompts', f'"{profile}", {0}')
    else:
        profile = toggle[0][0]
    
    stop_event = threading.Event()
    
    def run_cache_and_map():
        cache_and_map_with_retry(mount, output_loc)
        stop_event.set()
    
    thread = threading.Thread(target=run_cache_and_map)
    thread.start()
    
    while not stop_event.is_set():
        user_input = input("Type 'stop' to stop the process after the current operation: ").strip().lower()
        if user_input == 'stop':
            stop_event.wait()
            break
    
    open_cache_n_batch(output_loc, profile)

if __name__ == '__main__': 
    main()
