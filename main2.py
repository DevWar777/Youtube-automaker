# Author: Wolf-Rudiger Kotte
# Copyright 2022

# from fileinput import filename
import os 
import cv2  
from PIL import Image
from cv2 import VideoWriter  
from voicerobot import VoiceRobot
from cv2 import VideoWriter_fourcc
import numpy as np
import random
import mutagen
from mutagen.mp3 import MP3
from transition import Transition
from moviepy.video.compositing import CompositeVideoClip
from moviepy.editor import *


def mutagen_length(path):
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None

print(os.getcwd())  
  
# os.chdir("D://dev/python_youtube_maker_Spain/Auto_maker/images")    # you have to input your data url
path = "D://dev//python_youtube_maker_Spain//Auto_maker//images"       # you have to input your data url
  
mean_height = 0
mean_width = 0
  
num_of_images = len(os.listdir(path))

speech_filename = "text/speech.txt"   # input your subtitle text filename
speech_robot = VoiceRobot(speech_filename)
sent_info = speech_robot.text_to_speech()
speech_time = mutagen_length("output/speech.mp3")

padding = 2             # transition duration
fps_value = 1/ (((num_of_images-1)*padding + speech_time) / num_of_images)
print(num_of_images, speech_time, fps_value)
print('FPS:', fps_value)
  
for file in os.listdir(path): 
    im = Image.open(os.path.join(path, file)) 
    width, height = im.size 
    mean_width += width 
    mean_height += height 
    

mean_width = int(mean_width / num_of_images) 
mean_height = int(mean_height / num_of_images) 
mean_width = min(mean_width, 1920)
mean_height = min(mean_height, 1080)
  
  
for file in os.listdir(path): 
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
        
        im = Image.open(os.path.join(path, file))  
   
        
        width, height = im.size    
        print(width, height) 
  
        
        imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)  
        imResize.save( 'images_resized/' + file, 'JPEG', quality = 95) 
        
        print(file.split('\\')[-1], " is resized")  
  
  
def generate_video(): 
    image_folder = 'images_resized/'
    # video_name = 'output.avi'             # input your video filename
    # os.chdir('.')                                   # video output directory
      
    images = [img for img in os.listdir(path) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
     
    # images = [os.getcwd()]
    
    print(images)  
  
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
 
   
    height, width, layers = frame.shape   

    video_clips = []
    
    for image in images:
        videoname = image.split('.')[0] + '.avi'
        print(videoname)
        videopath = os.path.join(image_folder, '..', 'videos', videoname)
        video_clips.append(videopath)
        video = cv2.VideoWriter(videopath, 0, fps_value, (width, height))  
        video.write(cv2.imread('images_resized/' + image))
        video.release()

    effect(video_clips)
    final_video = speech_robot.add_speech('output/final.mp4', 'output/speech.mp3')
    final_video.write_videofile('output/sync.mp4', fps=25)
    return
        
    video_fx_list = [video_clips[0]]
    idx = video_clips[0].duration - padding
    for video in video_clips[1:]:
        video_fx_list.append(video.set_star(idx).crossfading(padding))
        idx += video.duration - padding
        
    final_video = CompositeVideoClip(video_fx_list)
    final_video.write_videofile('.', fps = np.CLIP.fps)
    # speech_filename = "speech.txt"   # your subtitle text filename
    # speech_robot = VoiceRobot()
    # speech = speech_robot.text_to_speech()    
    # final_video = speech_robot.add_speech(video_name, 'C:\\Python\\speech.mp3')
#    final_video.save()
    cv2.destroyAllWindows()  
    final_video.release()    

def effect(video_clips):
    padding = 2

    video_clips = [VideoFileClip(x) for x in video_clips]

    video_fx_list = [video_clips[0]]

    idx = video_clips[0].duration - padding
    for video in video_clips[1:]:
        video_fx_list.append(video.set_start(idx).crossfadein(padding))
        idx += video.duration - padding

    final_video = CompositeVideoClip(video_fx_list)
    final_video.write_videofile('output/final.mp4', fps=25)
  
# speech_filename = "speech.txt"   # your subtitle text filename
# speech_robot = VoiceRobot()
# speech = speech_robot.text_to_speech()
# print(speech.dura)
# exit(0)
generate_video() 








# =================================================================================

# print(os.getcwd())  
  
# os.chdir("D://dev/python_youtube_maker_Spain/Auto_maker/images")    # you have to input your data url
# path = "D://dev//python_youtube_maker_Spain//Auto_maker//images"       # you have to input your data url
  
# mean_height = 0
# mean_width = 0
  
# num_of_images = len(os.listdir(path)) 
  
# for file in os.listdir(path): 
#     im = Image.open(os.path.join(path, file)) 
#     width, height = im.size 
#     mean_width += width 
#     mean_height += height 
    
  
# mean_width = int(mean_width / num_of_images) 
# mean_height = int(mean_height / num_of_images) 
  
  
# for file in os.listdir(path): 
#     if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
        
#         im = Image.open(os.path.join(path, file))  
   
        
#         width, height = im.size    
#         print(width, height) 
  
        
#         imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)  
#         imResize.save( file, 'JPEG', quality = 95) 
        
#         print(file.split('\\')[-1], " is resized")  
  
  
# def generate_video(): 
#     image_folder = path
#     video_name = 'output.avi'             # input your video filename
#     os.chdir('.')                                   # video output directory
      
#     images = [img for img in os.listdir(path) 
#               if img.endswith(".jpg") or
#                  img.endswith(".jpeg") or
#                  img.endswith("png")] 
     
#     # images = [os.getcwd()]
    
#     print(images)  
  
#     frame = cv2.imread(os.path.join(image_folder, images[0])) 
 
   
#     height, width, layers = frame.shape   
  
#     video = cv2.VideoWriter(video_name, 0, 0.2, (width, height))  

#     padding = 2             # transition duration


#     for image in images:
#         video.write(cv2.imread(os.path.join(image_folder, image)))

        
      
#     # speech_filename = "speech.txt"   # your subtitle text filename
#     # speech_robot = VoiceRobot()
#     # speech = speech_robot.text_to_speech()    
#     # final_video = speech_robot.add_speech(video_name, 'C:\\Python\\speech.mp3')
# #    final_video.save()
#     cv2.destroyAllWindows()  
#     video.release()    
  
  
# generate_video() 