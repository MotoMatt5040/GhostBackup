from dotenv import load_dotenv, set_key
import os
import threading
import time
import shutil
from tkinter import filedialog
import re
import sys

load_dotenv(os.path.join(os.getcwd(), '.env'))

threads = []


def reset() -> None:
    print(
        'Running initial setup script:\n\nPlease select your save game directory.\n    --NOTE: This is the folder '
        'containing your save folders, not your single instance save folder.')
    save_path = filedialog.askdirectory()
    set_key('.env', 'save_game_dir', save_path)

    allowed_saves_count = input(
        'Please enter the amount of backup files you would like to be saved (> 1): ')
    while True:
        try:
            allowed_saves_count = int(allowed_saves_count)
            if allowed_saves_count < 2:
                raise ValueError
            break
        except:
            allowed_saves_count = input('Please enter a valid number > 1: ')

    set_key('.env', 'allowed_saves_count', str(allowed_saves_count))

    while True:
        try:
            save_interval = int(input('Please enter the amount of time between backups in minutes (> 0): ')) * 60
            if save_interval < 0:
                raise ValueError
            break
        except:
            print('Please enter a valid number.\n')

    set_key('.env', 'save_interval', str(save_interval))

    input('Setup complete, please press enter to close the program and run the program again.')


def backup(force=False) -> None:
    save_path = os.environ.get('save_game_dir')
    allowed_saves_count = os.environ.get('allowed_saves_count')
    saves = os.listdir(save_path)

    def extract_number(filename):
        if filename == saves[0]:
            return -float('inf')
        match = re.search(r'(\d+)', filename)
        return int(match.group(0)) if match else float('inf')

    if len(saves) == 1:
        original_save = os.path.join(save_path, saves[0])
        backup_save = os.path.join(save_path, f'{saves[0]}-2')
        shutil.copytree(original_save, backup_save)

    while True:
        saves = os.listdir(save_path)
        saves = sorted(saves, key=lambda x: (extract_number(x), x))

        amount_to_delete = len(saves) - int(allowed_saves_count)

        if amount_to_delete > 0:
            for i in range(1,
                           amount_to_delete + 1):  # +1 is used here so that -latest will be the final entry in the dir
                shutil.rmtree(os.path.join(save_path, saves[i]))
                # print(f"Deleted: {os.path.join(save_path, saves[i])}")

        remaining_saves = os.listdir(save_path)
        remaining_saves = sorted(remaining_saves, key=lambda x: (extract_number(x), x))

        new_save_index = 2
        # print(remaining_saves)
        for save in remaining_saves:
            if save == saves[0] or save == f'{saves[0]}-latest':
                continue
            new_name = f'{saves[0]}-{new_save_index}'
            old_path = os.path.join(save_path, save)
            new_path = os.path.join(save_path, new_name)
            os.rename(old_path, new_path)
            new_save_index += 1

        saves = os.listdir(save_path)
        saves = sorted(saves, key=lambda x: (extract_number(x), x))
        target_backup_name = saves[-1]

        target_file = f'{save_path}/{target_backup_name}'
        target_rename = f"{save_path}/{target_backup_name.replace('-latest', f'-{len(saves)}')}"
        os.rename(target_file, target_rename)

        target_backup_name = target_backup_name.replace('-latest', f'-{len(saves)}')

        target_file = f'{save_path}/{saves[0]}'
        target_rename = f'{save_path}/{target_backup_name.replace(f"-{len(saves)}", "-latest")}'
        shutil.copytree(target_file, target_rename)

        if force:
            print(f'Forced backup complete.')
            return

        save_interval = os.environ.get('save_interval')
        if not save_interval:
            time.sleep(900)
            continue
        time.sleep(float(save_interval))


def restore(restore_type=None) -> None:
    save_path = os.environ['save_game_dir']
    saves = os.listdir(save_path)
    original_save_dir = saves[0]
    shutil.rmtree(f'{save_path}/{original_save_dir}')
    if not restore_type:
        backup_save_dir = saves[-1]
        shutil.copytree(f'{save_path}/{backup_save_dir}', f'{save_path}/{original_save_dir}')
    else:
        backup_save_dir = filedialog.askdirectory(title="Select backup save game to restore.")
        shutil.copytree(f'{backup_save_dir}', f'{save_path}/{original_save_dir}')

    print(f'Restore complete.')


def interface():
    while True:
        print('Available commands.')
        print('p     reset save path')
        print('r     restore latest save')
        print('b     force backup')
        try:
            option = input().lower()
            match option:
                case 'p':
                    reset()
                    sys.exit()
                case 'r':
                    restore_type = input(
                        "Press enter for latest, or type [s] to select a specific backup: [enter]/[s]\n\n")
                    restore(restore_type)
                case 'b':
                    backup(True)
                case _:
                    print('Invalid option.')
        except:
            import traceback
            print(traceback.format_exc())
            print('Invalid option.')


if not os.environ.get('save_game_dir'):
    reset()
    sys.exit()

if __name__ == "__main__":
    threads.append(threading.Thread(target=backup))
    threads.append(threading.Thread(target=interface))

    for thread in threads:
        thread.daemon = True
        thread.start()
    while True:
        pass
