from dotenv import load_dotenv, set_key
load_dotenv()

import os
import threading
import time
import shutil
import msvcrt
import tkinter as tk
from tkinter import filedialog
import re

threads = []


def reset() -> None:
    print('Running initial setup script:\n\nPlease select your save game directory.\n    --NOTE: This is the folder containing your save folders, not your single instance save folder.')
    save_path = filedialog.askdirectory()
    set_key('.env', 'save_game_dir', save_path)

    allowed_saves_count = input('Please enter the amount of backup files you would like to be saved.')
    set_key('.env', 'allowed_saves_count', allowed_saves_count)

    save_interval = input('Please enter the amount of time between backups in minutes: ')
    set_key('.env', 'save_interval', save_interval * 60)

    input('Setup complete, please close and run script again to save state.')


def backup() -> None:
    def extract_number(filename):
        if filename == 'Save':
            return -float('inf')
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else float('inf')

    save_path = os.environ.get('save_game_dir')
    allowed_saves_count = os.environ.get('allowed_saves_count')
    saves = os.listdir(save_path)

    if len(saves) == 1:
        original_save = os.path.join(save_path, saves[0])
        backup_save = os.path.join(save_path, f'{saves[0]}-2')
        shutil.copytree(original_save, backup_save)

    while True:
        saves = os.listdir(save_path)
        saves = sorted(saves, key=lambda x: (extract_number(x), x))

        if len(saves) > int(allowed_saves_count):
            shutil.rmtree(os.path.join(save_path, saves[1]))
            for i in range(1, int(allowed_saves_count)):
                file_to_change = os.path.join(save_path, saves[i + 1])
                name_to_change_to = os.path.join(save_path, saves[i])
                os.rename(file_to_change, name_to_change_to)

        saves = os.listdir(save_path)
        saves = sorted(saves, key=lambda x: (extract_number(x), x))
        print(saves)
        target_backup = saves[-1]

        target_file = f'{save_path}/{target_backup}'
        target_rename = f"{save_path}/{target_backup.replace('-latest', f'-{len(saves)}')}"
        os.rename(target_file, target_rename)

        target_backup = target_backup.replace('-latest', f'-{len(saves)}')

        target_file = f'{save_path}/{target_backup}'
        target_rename = f'{save_path}/{target_backup.replace(f"{len(saves)}", "latest")}'
        shutil.copytree(target_file, target_rename)

        time.sleep(5)


def restore(restore_type=None) -> None:
    save_path = os.environ['save_game_dir']
    saves = os.listdir(save_path)
    if not restore_type:
        backup_file_path = saves[-1]
        original_save_dir = saves[0]
    else:
        backup_file_path = filedialog.askdirectory(title="Select backup to restore to.")
        original_save_dir = saves[0]
    shutil.rmtree(original_save_dir)
    shutil.copytree(f'{backup_file_path}', f'{original_save_dir}')
    print(f'Restore complete.')


def interface():
    print('Available commands.')
    print('p     reset save path')
    print('r     restore latest save')
    while True:
        try:
            option = input().lower()
            match option:
                case 'p':
                    reset()
                case 'r':
                    restore_type = input("Press enter for latest, or type 'select' to select a specific backup")
                    restore(restore_type)
                case _:
                    print('Invalid option.')
        except:
            print('Invalid option.')


if not os.environ.get('save_game_dir'):
    reset()

if __name__ == "__main__":
    threads.append(threading.Thread(target=backup))
    threads.append(threading.Thread(target=interface))

    for thread in threads:
        thread.start()
