from dotenv import load_dotenv, set_key

load_dotenv()

import os
import threading
import time
import shutil
import msvcrt
import tkinter as tk
from tkinter import filedialog

threads = []


def reset() -> None:
    print('Running initial setup script:\n\nPlease select your save game directory.\n    --NOTE: This is the folder '
          'containing your save folders, not your single instance save folder.')
    save_path = filedialog.askdirectory()
    set_key('.env', 'save_game_dir', save_path)

    allowed_saves_count = input('Please enter the amount of backup files you would like to be saved: ')
    set_key('.env', 'allowed_saves_count', allowed_saves_count)

    save_interval = input('Please enter the amount of time between backups in minutes: ')
    set_key('.env', 'save_interval', save_interval * 60)

    input('Setup complete, please close and run script again to save state.')


def backup() -> None:
    while True:
        save_path = os.environ.get('save_game_dir')
        save_interval = os.environ.get('save_interval')
        saves = os.listdir(save_path)

        if len(saves) > int(os.environ['allowed_saves_count']):
            os.mkdir(os.path.join(save_path, 'temp'))
            shutil.copytree(f'{save_path}/{saves[0]}', f'{os.path.dirname(save_path)}/temp/{saves[0]}')
            # save_path = f"{os.path.dirname(save_path)}/temp"

        target_backup = saves[-1]
        os.rename(f'{save_path}/{target_backup}', f"{save_path}/{target_backup.replace('-latest', f'-{len(saves)}')}")
        target_backup = target_backup.replace('-latest', f'-{len(saves)}')
        shutil.copytree(f'{save_path}/{target_backup}',
                        f'{save_path}/{target_backup.replace(f"{len(saves)}", "latest")}')
        time.sleep(float(save_interval))


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
