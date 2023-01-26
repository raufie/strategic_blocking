from win10toast import ToastNotifier
from pathlib import Path

import wave
import sys

import threading

from pydub.playback import play
from pydub import AudioSegment, playback

import time


class Notifications:
    def __init__(self, path):
        self.toast = ToastNotifier()
        self.audio_thread = None
        self.is_playing = False
        self.path = path

    def show_notification(self, time_amount):
        self.toast.show_toast(
            "Strategic Blocking",
            f"Time Block Over: {int(time_amount)} seconds",
            duration=10,
            threaded=True,
            icon_path=''
        )
        self.play_sound(self.path)
        while self.toast.notification_active():
            time.sleep(0.1)
        self.stop_audioprocess()

    def play_sound(self, path):
        print("playing sound")

        # playsound(path)   # audio = + "/" + file
        # print(audio)
        # playsound(audio)

        # sound = AudioSegment.from_mp3(path)
        # pay(sound)
        if self.is_playing:
            self.stop_audioprocess()
            return False

        else:
            self.audio_thread = threading.Thread(
                target=lambda: self.audio_process(path), args=())
            self.audio_thread.start()
            return True

    def audio_process(self, path):
        a = AudioSegment.from_mp3(path)
        self.audio_object = playback._play_with_simpleaudio(a)
        self.is_playing = True
        # play(self.audio_object)

    def stop_audioprocess(self):
        self.is_playing = False
        self.audio_object.stop()
        # def _play_with_ffplay(seg):
        # self.audio_thread.
