#############################################################
#   This is a Youtube Video Automaker for Praedium          #
#   Author: Wolf-Rudiger Kotte                              #
#   Copyright 2022                                          #
#############################################################

import os
import shutil
import cv2
import codecs
import pyttsx3
import numpy as np
from gtts import gTTS
from mutagen.mp3 import MP3
import audioread
from moviepy.editor import concatenate_audioclips, AudioFileClip, VideoFileClip
from moviepy.video.compositing import CompositeVideoClip
from moviepy.editor import *
import moviepy.editor as mpe
from PIL import ImageFont, ImageDraw, Image

IMAGE_PATH = 'image/'
SPEECH_PATH = 'text/ejemplo.txt'

MAX_SUBTITLE_LENGTH = 60
MAX_SUBTITLE_LINELENGTH = 35
VIDEO_WIDTH = 1920; VIDEO_HEIGHT = 1080
# VIDEO_WIDTH = 320; VIDEO_HEIGHT = 240
VIDEO_FPS = 25
EFFECT_DURATION = 2
AUDIO_PADDING_END = 0

os.makedirs('audio', exist_ok=True)
os.makedirs('video', exist_ok=True)

def split_text(txt):
    subtitles = []

    for line in txt.splitlines():
        if line == '': continue
        line = line.strip()
        if line == '': continue

        while True:
            p = line.find(' ', MAX_SUBTITLE_LENGTH)
            if p == -1:
                subtitles.append(line + '\n')
                break
            else:
                subtitles.append(line[:p])
                line = line[p+1:]

    return subtitles

def concatenate_audio(audio_paths, output_path):
    clips = [AudioFileClip(x) for x in audio_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)

def concatenate_video(video_paths, output_path):
    clips = [VideoFileClip(x) for x in video_paths]

    effect_list = [clips[0]]
    effect_time = effect_list[-1].duration - EFFECT_DURATION
    for clip in clips:
        effect_list.append(clip.set_start(effect_time).crossfadein(EFFECT_DURATION))
        effect_time += clip.duration - EFFECT_DURATION

    final_clip = CompositeVideoClip(effect_list)
    final_clip.write_videofile(output_path, fps=VIDEO_FPS)

def composite_video_audio(video_path, audio_path, output_path):
    video = mpe.VideoFileClip(video_path)
    audio = mpe.AudioFileClip(audio_path)
    final = video.set_audio(audio)
    final.write_videofile(output_path, fps=VIDEO_FPS)

def total_speech(SPEECH_PATH):
        f = open(SPEECH_PATH, 'r')
        mytext = f.read()
        f.close()
        
        total_text_to_speech = pyttsx3.init()
        total_text_to_speech.setProperty('rate', 150)
        voices = total_text_to_speech.getProperty('voices')
        total_text_to_speech.setProperty('voice', voices[2].id)       
        total_text_to_speech.setProperty('voice', 'spanish')
        total_text_to_speech.say(mytext)
        total_text_to_speech.save_to_file(mytext, 'audio/speech.mp3')
        total_text_to_speech.runAndWait()

        total_audio = audioread.audio_open('audio/speech.mp3')
        audio1_length = total_audio.duration
        print(audio1_length)
        total_audio.close()
        
        # audio = gTTS(text=mytext, lang="es", slow=False)  # 
        # audio.save("audio/speech.mp3")
        # os.system("start speech.mp3")

total_speech(SPEECH_PATH)

# Read text & Split into subtitles
fp = codecs.open(SPEECH_PATH, 'r', 'utf-8')
subtitles = split_text(fp.read())
fp.close()

# Convert subtitles to audios & Concatenate audios
audio_paths = []
audio_lengths = []
for idx, subtitle in enumerate(subtitles):
    end_of_line = False
    if subtitle[-1] == '\n':
        subtitle = subtitle[:-1]
        end_of_line = True

    audio_path = f'audio/{idx}.mp3'
    audio_paths.append(audio_path)

    # set voice and reading speed
    text_to_speech = pyttsx3.init()
    text_to_speech.setProperty('rate', 150)
    voices = text_to_speech.getProperty('voices')

    # for voice in voices:
    #     # to get the info. about various voices in our PC 
    #     print("Voice:")
    #     print("ID: %s" %voice.id)
    #     print("Name: %s" %voice.name)
    #     print("Age: %s" %voice.age)
    #     print("Gender: %s" %voice.gender)
    #     print("Languages Known: %s" %voice.languages)
    
    text_to_speech.setProperty('voice', voices[2].id)
    text_to_speech.setProperty('voice', 'spanish')
    text_to_speech.say(subtitle)
    text_to_speech.save_to_file(subtitle, audio_path)
    text_to_speech.runAndWait()

    audio = audioread.audio_open(audio_path)
    audio_length = audio.duration
    audio.close()

    if not end_of_line:
        audio_length -= 0.55
        #audio = mpe.AudioFileClip(audio_path)
        #audio.set_duration(audio_length)
        #audio.write_audiofile(audio_path)

    audio_lengths.append(audio_length)
#concatenate_audio(audio_paths, 'audio/final.mp3')

audio_final_length = sum(audio_lengths)

# List images in directory & Calculate parameters
image_paths = os.listdir(IMAGE_PATH)

image_n = len(image_paths)
fps = 1 / ((audio_final_length + (EFFECT_DURATION * (image_n - 1)) - AUDIO_PADDING_END) / image_n)

# Convert images to videos & Concatenate videos using effect
video_paths = []
for idx, image_name in enumerate(image_paths):
    image = cv2.imread(os.path.join(IMAGE_PATH, image_name))
    image = cv2.resize(image, (VIDEO_WIDTH, VIDEO_HEIGHT))

    video_path = f'video/{idx}.avi'
    video_paths.append(video_path)
    videoWriter = cv2.VideoWriter(video_path, 0, fps, (VIDEO_WIDTH, VIDEO_HEIGHT))
    videoWriter.write(image)
    videoWriter.release()
concatenate_video(video_paths, 'video/final_1.mp4')

# Draw text on video
videoCapture = cv2.VideoCapture('video/final_1.mp4')
videoWriter = cv2.VideoWriter('video/final_2.avi', 0, VIDEO_FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))

font_path = 'text/consola.ttf'
font = ImageFont.truetype(font_path, 52)

frame_idx = -1
while True:
    ret, image = videoCapture.read()
    frame_idx += 1
    if not ret:
        break
    subtitle = ''
    for i in range(len(subtitles)):
        frame_time = frame_idx / VIDEO_FPS
        if frame_time < sum(audio_lengths[:i+1]):
            subtitle = subtitles[i]
            break
    if len(subtitle) > MAX_SUBTITLE_LINELENGTH:
        subtitle = subtitle[:MAX_SUBTITLE_LINELENGTH] + '\n' + subtitle[MAX_SUBTITLE_LINELENGTH:]

    # set subtitle backdrop & text position & font-family & font-color
    if subtitle != '':
        image[VIDEO_HEIGHT-210:VIDEO_HEIGHT-90, 320:1380] //= 2
        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)
        # draw.rectangle([(340, VIDEO_HEIGHT-200), (100, 40)], fill=(0, 0, 0, 170), outline=None)
        draw.text((340, VIDEO_HEIGHT - 200), subtitle, font=font, fill=(255, 255, 255, 255))
        image = np.array(image_pil)
    videoWriter.write(image)

    
videoCapture.release()
videoWriter.release()

# Composite Video & Audio
composite_video_audio('video/final_2.avi', 'audio/speech.mp3', 'final.mp4')

shutil.rmtree('audio')
shutil.rmtree('video')
