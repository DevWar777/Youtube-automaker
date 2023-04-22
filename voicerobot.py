#############################################################
#   This is a Youtube Video Automaker for Praedium          #
#   Author: Top Developer                                   #
#   Copyright 2022                                          #
#############################################################

from gtts import gTTS
from collections.abc import Sequence
import os
import moviepy.editor as mpe
import ffmpeg
import nltk
from pydub import AudioSegment


class VoiceRobot():

    def __init__(self, filename):
        self.filename = filename


    def text_by_sentence(self):
        with open(self.filename, 'w', encoding = "utf-8") as in_file:
            text = in_file.read()
            # sents = nltk.sent_tokenize(text)
            
            

        print(sents)
        return sents

        # sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)


    def text_to_speech(self):
        # f = open(self.filename, 'r')
        # mytext = f.read()
        # audio = gTTS(text=mytext, lang="es", slow=False)
        # audio.save("output/speech.mp3")
        # os.system("start speech.mp3")
        
        # mytext = []
        sents = self.text_by_sentence()
        for sent in sents:
            audio_sent = gTTS(text=sent, lang="es", slow=False)
            


        return audio
    
    def add_speech(self, video_file, speech_file):
        my_clip = mpe.VideoFileClip(video_file)
        audio_background = mpe.AudioFileClip(speech_file)
        #final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
        final_clip = my_clip.set_audio(audio_background)
        return final_clip

    