import os
import time
import pygame
from mutagen.mp3 import MP3

def play_badapple():

# Config
    mp3_file = "src/badapple/audio.mp3"
    frames_folder = "src/badapple/frames/"

    # Get audio duration
    audio = MP3(mp3_file)
    duration = audio.info.length  # in seconds

    # Load frames
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(".txt")])
    total_frames = len(frame_files)

    # Calculate FPS
    fps = 32#total_frames / duration
    frame_delay = 1 / fps

    print(f"Total frames: {total_frames}")
    print(f"Audio duration: {duration:.2f}s")
    print(f"Calculated FPS: {fps:.2f} ({frame_delay:.3f}s per frame)")

    # Initialize Pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)

    # Play music
    pygame.mixer.music.play()
    start_time = time.time()

    # Show frames
    for frame_name in frame_files:
        os.system("cls" if os.name == "nt" else "clear")  # Cross-platform clear
        with open(os.path.join(frames_folder, frame_name), "r", encoding="utf-8") as f:
            print(f.read())
        time.sleep(frame_delay)

    # Wait for music to finish if needed
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
