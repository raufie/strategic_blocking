import msvcrt
import os
import time
import keyboard
import threading
from win10toast import ToastNotifier
import sys


class PromptManager:
    def __init__(self):
        self.toast = ToastNotifier()
        self.pressed = "N"
        # N, C, P

    def start_up(self):
        print(
            "\u001b[35m**** "*4+"Welcome to the Systematic Blocker"+"****  "*4)

    # DECORATORS
    def _cleaner_print(prompt_func):
        def wrapped(self, *args, **kwargs):
            print("\u001b[0m", end="")
            to_return = prompt_func(self, *args, **kwargs)
            print("\u001b[0m", end="")
            return to_return
        return wrapped

    # THREADs callbacks
    def inputThread(self):
        op = msvcrt.getch().strip()
        if op == b"p" or op == b"P":
            self.update_state("P")
        elif op == b"c" or op == b"C":
            self.update_state("C")

        # base CLASS METHODS

    def update_state(self, state):
        self.pressed = state
# prompt methods

    @ _cleaner_print
    def get_task_info(self):
        print("Please type in the category for your task: \u001b[33m", end="")
        category = input()
        category = "DEFAULT" if category == "" else category

        return category.strip()

    @ _cleaner_print
    def waiting_prompt(self, time_amount=5.0, block_number=0):
        """
            @dev: this function confirms whether the user wants to start the task or not
            The user shall be able to cancel at any moment.. the function returns neagative and nothing will be added
            or the function returns the time to be added
        """

        # X: exit
        # S: start
        # Y: yes
        # N: no
        # C cancel
        #
        print(
            "Press [S] to start timer. Press [X] to exit app. Press [T] to view today's time worked")
        op = msvcrt.getch().strip()

        if op == b"X" or op == b"x":
            print("EXITING PROGRAM...")
            del self.toast
            sys.exit()
        elif op == b"t" or op == b"T":

            print("Viewing today's total time worked (in seconds)...")
            return {'time': -5.0}
        elif op == b"S" or op == b"s":
            confirmed = self.confirm_prompt()
            if confirmed:
                os.system("cls")
                print("Starting Timer Now...")
                print(
                    "Press \u001b[31m [C] \u001b[0m to cancel the timer anytime!")
                print(
                    "Press \u001b[32m [P] \u001b[0m to cancel the timer and save the already worked time")
                start_time = time.time()

                # in time loop

                # keyboard.on_press_key("c", lambda x: self.update_state("C"))
                # keyboard.on_press_key("C", lambda x: self.update_state("C"))
                # keyboard.on_press_key("p", lambda x: self.update_state("P"))
                # keyboard.on_press_key("P", lambda x: self.update_state("P"))
                t1 = threading.Thread(target=self.inputThread, args=())
                t1.start()
                while True:
                    # op = msvcrt.getch().strip()
                    if self.pressed == "C":
                        self.update_state("N")
                        print("Cancelling Timer...")
                        return {'time': -1.0}

                    if self.pressed == "P":
                        self.update_state("N")
                        return {'time': time.time() - start_time, 'timestamp': time.time()}

                    print("\r"+str(int(time.time() - start_time) // 60) +
                          "m" + str(int(time.time() - start_time) % 60)+"s", end="")

                    # TIME's UP
                    if time.time() > start_time + time_amount:
                        print()
                        # NOTIFY
                        self.toast.show_toast(
                            "Strategic Blocking",
                            f"Time Block Over: {int(time_amount)} seconds",
                            duration=10,
                            threaded=True,
                            icon_path=''
                        )
                        return {'time': time_amount, 'timestamp': time.time()}
                    time.sleep(1.0)

            else:
                return {'time': -1.0}
        else:
            return {'time': -1.0}

    @ _cleaner_print
    def confirm_prompt(self):
        print("Are you sure? [Y] for yes, anything else for no [N]")
        op = msvcrt.getch().strip()
        if op == b"y" or op == b"Y":
            return True
        else:
            return False

    @ _cleaner_print
    def time_prompt_loop(self, _op):
        pass
