#!/usr/bin/env python3

# see: https://www.daniweb.com/programming/software-development/code/216976/play-a-midi-music-file-using-pygame

# sudo pip install pygame

# on ubuntu
# sudo apt-get install python-pygame

import sys

import pygame

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        sys.stdout.write(f"Music file {music_file} loaded\n")
    except pygame.error:
        sys.stdout.write(f"File {music_file} not found! - {pygame.get_error()}\n")
        return 1
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
    return 0

def main():
    # pick a midi music file you have ...
    # (if not in working folder use full path)
    if len(sys.argv) != 2:
        sys.stderr.write("Invalid arguments\n")
        sys.stdout.write(f"Usage: ./{__file__.split('/')[-1]} <midi_file_path>\n")
        return 1

    midi_file = sys.argv[1]
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    try:
        play_music(midi_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
    return 0

if __name__ == '__main__':
    sys.exit(main())
