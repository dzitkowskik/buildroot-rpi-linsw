import pygame as pg
 
def play_music(music_file, volume=0.8):
    # set up the mixer
    freq = 44100 # audio CD quality
    bitsize = -16 # unsigned 16 bit
    channels = 2 # 1 is mono, 2 is stereo
    buffer = 2048 # number of samples (experiment to get best sound)

    pg.mixer.init(freq, bitsize, channels, buffer)

    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! ({})".format(music_file, pg.get_error()))
        return
    pg.mixer.music.play()
    while pg.mixer.music.get_busy():
        clock.tick(30)

music_file = "/root/bandoleros.mp3"
volume = 0.8
play_music(music_file, volume)
