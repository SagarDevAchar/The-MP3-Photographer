import cv2
import numpy as np
from tqdm import trange
from os import listdir
from time import sleep


def get_stegano_or(mp3: bytes):
    or_arr = np.zeros((1, W * H * 3), dtype=np.uint8)
    # or_arr = np.random.randint(0, 256, (H, W, 3), dtype=np.uint8) & 0x03
    i = W * H * 3 - len(mp3) * 4
    for x in trange(len(mp3), ncols=100, unit=' bytes', desc='\t'):
        b = mp3[x]
        or_arr[0, i+0] = (b & 0b11000000) >> 6
        or_arr[0, i+1] = (b & 0b00110000) >> 4
        or_arr[0, i+2] = (b & 0b00001100) >> 2
        or_arr[0, i+3] = (b & 0b00000011) >> 0
        i += 4

    return np.reshape(or_arr, (H, W, 3))


SECTION_SEPERATOR = '\n' + '-' * 169 + '\n'

LOGO = """
    ████████╗██╗  ██╗███████╗    ███╗   ███╗██████╗ ██████╗     ██████╗ ██╗  ██╗ ██████╗ ████████╗ ██████╗  ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██████╗ 
    ╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗╚════██╗    ██╔══██╗██║  ██║██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔════╝██╔══██╗
       ██║   ███████║█████╗      ██╔████╔██║██████╔╝ █████╔╝    ██████╔╝███████║██║   ██║   ██║   ██║   ██║██║  ███╗██████╔╝███████║██████╔╝███████║█████╗  ██████╔╝
       ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔═══╝  ╚═══██╗    ██╔═══╝ ██╔══██║██║   ██║   ██║   ██║   ██║██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
       ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║     ██████╔╝    ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝     ╚═════╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

                                                 █▀▄ █ █   █▀▀ █▀█ █▀▀ █▀█ █▀▄   █▀▄ █▀▀ █ █   █▀█ █▀▀ █ █ █▀█ █▀▄
                                                 █▀▄  █    ▀▀█ █▀█ █ █ █▀█ █▀▄   █ █ █▀▀ ▀▄▀   █▀█ █   █▀█ █▀█ █▀▄
                                                 ▀▀   ▀    ▀▀▀ ▀ ▀ ▀▀▀ ▀ ▀ ▀ ▀   ▀▀  ▀▀▀  ▀    ▀ ▀ ▀▀▀ ▀ ▀ ▀ ▀ ▀ ▀
""" + SECTION_SEPERATOR

print(LOGO)

print("INSTRUCTIONS\n")
print("1.\tPlace the JPG files with '<filename>.jpg' in the adjacent directory labeled 'IN'")
print("2.\tPlace the MP3 files with '<filename>.mp3' in the adjacent directory labeled 'IN'")
print("3.\tWell, that's it, run this code")

print("\n<filename.png> will be available in the adjacent directory labeled 'SRC'")

print(SECTION_SEPERATOR)

input('Press ENTER to start the conversion process...')

W, H = 1280, 720

SONG_NAMES = []
for filename in listdir('IN'):
    filename = filename.split('.')
    if filename[1] == 'jpg':
        SONG_NAMES.append(filename[0])

print('\nJPG Files Found = %d' % len(SONG_NAMES))

print(SECTION_SEPERATOR)

for SONG_NAME in SONG_NAMES:
    try:
        IMAGE = cv2.resize(cv2.imread("IN/%s.jpg" % SONG_NAME, cv2.IMREAD_COLOR), (W, H))
        AUDIO = open("IN/%s.mp3" % SONG_NAME, 'rb').read()

        print(f"\nWriting {SONG_NAME:s}.mp3 into of {SONG_NAME:s}.png")

        assert len(AUDIO) <= W * H * 3 / 4
        sleep(0.1)

        STEGANO_ERASED_IMAGE = IMAGE & 0b11111100
        STEGANO_OR = get_stegano_or(AUDIO)
        STEGANO_WRITTEN_IMAGE = STEGANO_ERASED_IMAGE | STEGANO_OR

        cv2.imwrite(f'SRC/{SONG_NAME:s}.png', STEGANO_WRITTEN_IMAGE)
    except AssertionError:
        print("ERROR: Cannot create %s.png! MP3 is too big for the JPG" % SONG_NAME)
    except Exception as e:
        print("ERROR:   Failed to create %s.png! Encountered the following error: %s" % (SONG_NAME, str(e)))

print(SECTION_SEPERATOR)

input('Press ENTER to terminate...')
