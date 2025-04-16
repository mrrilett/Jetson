# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 18:21:31 2023

@author: micha
"""

#created on 2023-04-16 author @sabrina
#MIT Open Source Initiative License 
##############################################
##############################################
#
##
#Problem/Challenge:
#Import songs from youtube and make the Robot dance to them
#
# requirements: 
#               pip install youtube_search
#               pip install python_vlc
#               pip install pytube
#               pip install tempocnn
#               instalation of 64 bit (32 will not work) version of VLC https://get.videolan.org/vlc/3.0.11/win64/vlc-3.0.11-win64.exe
#              
#
#
#---------------importing modules-----------------------

from __future__ import unicode_literals
# import youtube_dl
import xarm #robotic arm module
import time 
import threading
from youtube_search import YoutubeSearch
import vlc
import librosa
import numpy as np
from moviepy.editor import AudioFileClip
import matplotlib.pylab as plt
import yt_dlp
# import sounddevice as sd
# import tempocnn
# from tempocnn.classifier import TempoClassifieras it
# from tempocnn.feature import read_features

#------------initializing variables--------------------------
arm = xarm.Controller('USB')
# arm.setPosition([[1,0.0],[1,0.0],[1,0.0],[1,0.0],[1,0.0],[1,0.0]])
TIME = 40 #seconds song will play


#--------------functions------------------------------------7
def downloadVideo(url):

        
    print('here')
    # YouTube(url).streams.get_audio_only().download()
    with yt_dlp.YoutubeDL({'format': 'mp4',
                            'outtmpl': '%(title)s.mp4'}) as ydl:
        # ydl.download([url])
        info = ydl.extract_info(url)
        title = info.get('title', 'Unknown Title')
    # break
    
            
 
    print(title)

    return (title+'.mp4')
# # initialize the model (may be re-used for multiple files)
    # classifier = TempoClassifier('model')
def dance(file):
    global TIME
    
    # # read the file's features
    # features = read_features(file)

    # # estimate the global tempo
    # tempo = classifier.estimate_tempo(features, interpolate=False)
    # # map beat to arm movements
   

def playAudio(file):
        
    global TIME
    arm.setPosition([[1,0.0],[1,0.0],[1,0.0],[1,0.0],[1,0.0],[1,0.0]])

    media_player = vlc.MediaPlayer()
    media = vlc.Media(file)
    media_player.set_media(media)
    
    r = int(0)
    i = [270,550]
    j = [200,500]
    k = [220,580]

    beats = beats_detect(file)
    media_player.audio_set_volume(70)
    media_player.play()
    time.sleep(1.4)
    for x,y in enumerate(beats):
        if y < 30:
            delta = beats[x+1] - beats[x]
            print(delta)
            time.sleep(delta)
            arm.setPosition(6,i[r],wait=False)
            arm.setPosition(3,j[r],wait=False)
            arm.setPosition(2,k[r],wait=False)
            
            if r==1:
                r = 0
            elif r==0:
                    r =1
            else:
            
                break

        
        
    # creating vlc media player object
        dance_thread = threading.Thread(target=dance, args=([file]))
        dance_thread.daemon = True 
        
        
        start_time = time.time()
        #time.sleep(0.1)
        current_time = time.time()
        if current_time - start_time > 40:
            media_player.stop()
        
   
    #time.sleep(TIME)
    
    #let song play for TIME seconds
    
    
def beats_detect(file):
    # audio, sr = extract_audio_from_video(file)
# Calculate the tempo and beats
    audio = AudioFileClip(file)
    audio_file = 'extracted_audio.wav'  # Path to save the extracted audio
    audio.write_audiofile(audio_file)
    y,sr = librosa.load(audio_file)
    # onset_env = librosa.onset.onset_strength(y=y,sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Plot the waveform and beats
    tempo,beat_frames = librosa.beat.beat_track(y=y,sr=sr)
    beat_times = librosa.frames_to_time(beat_frames,sr=sr)
    
    # plt.figure(figsize=(12, 6))
    # librosa.display.waveshow(y, sr=sr, alpha=0.5)
    # plt.vlines(beat_times, -1, 1, color='r', alpha=0.9, linestyle='--', label='Beats')
    # plt.title(f'Beat Detection - Tempo: {tempo:.2f} BPM')
    # plt.xlabel('Time')
    # plt.legend()
    # plt.show()
    
    # beat_times = librosa.frames_to_time(beats)
    print("detected beat timestamps in seconds ")
    return beat_times

#--------------------main-------------------------------------  


song_name = input("enter song name")
results = YoutubeSearch(song_name, max_results=10).to_dict() #put results in a dictionary

v = results.pop(0) #pop the first result from the result list
url = ('https://www.youtube.com' + v['url_suffix'])

file = downloadVideo(url)


playAudio(file)
