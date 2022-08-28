from PromptManager import PromptManager
from DataManager import DataManager
from TimerConfigurator import TimerConfigurator

import os
import json


def get_time_string(time_amount):
    return str(int(time_amount) // 60)+"m" + str(int(time_amount) % 60)+"s"


def main():
    os.system('cls')
    has_ended = False
    category = ""
    # block counter tells you what block of work u are on
    block_counter = 0
    prompts = PromptManager()
    prompts.start_up()

    timer_configurator = TimerConfigurator(".")
    data_manager = DataManager(timer_configurator.data['path'])

    category = prompts.get_task_info()
    try:
        config = timer_configurator.to_list()
    except Exception as e:
        config = [5*60, 30*60]  # default : 5 minutes start, 30 minutes main

    # while not has_ended:
    prev_time = 0
    while(True):

        # print priv data info
        if (block_counter > 0):
            print("Block Finished... "+get_time_string(prev_time))

        print("\u001b[33mNext Block# \u001b[0m " + str(block_counter+1))
        time_amount = config[0] if block_counter == 0 else config[1]
        print("\u001b[33mBlock Length# \u001b[0m " +
              get_time_string(time_amount))

        prompt_result = prompts.waiting_prompt(time_amount, block_counter+1)
        if prompt_result['time'] != None and prompt_result['time'] > 0.0:
            # SAVE TIME
            data_manager.add_data({
                "time_amount": prompt_result['time'],
                "timestamp": prompt_result['timestamp'],
                "category": category
            })
            prev_time = prompt_result['time']
            data_manager.save()
            block_counter += 1

        os.system("cls")


if __name__ == "__main__":
    main()
