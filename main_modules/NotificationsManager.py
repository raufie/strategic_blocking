from win10toast import ToastNotifier
from pathlib import Path

import wave
import sys

import pyaudio


class Notifications:
    def __init__(self):
        self.toast = ToastNotifier()

    def show_notification(self, time_amount):
        self.toast.show_toast(
            "Strategic Blocking",
            f"Time Block Over: {int(time_amount)} seconds",
            duration=10,
            threaded=True,
            icon_path=''
        )
        # self.play_sound()

    def play_sound(self, path):
        # print("playing sound")
        # playsound(path)   # audio = + "/" + file
        # print(audio)
        # playsound(audio)

        # sound = AudioSegment.from_mp3(path)
        # play(sound)
        pass
