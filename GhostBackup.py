import os
import shutil
import msvcrt
import tkinter as tk
from tkinter import filedialog

def check_dir():
    """
    Change working dir to savegame directory if savegamedir.txt is defined,
    else ask for the savegame directory with GUI.

    Parameters
    ----------
    None.

    Returns
    ----------
    None.
    """

    try:
        if os.path.isfile("savegamedir.txt"):
            with open("savegamedir.txt", 'r') as f:
                path = f.readlines()[0]
        else:
            with open("savegamedir.txt", 'w+') as f:
                print("Select your GRW save game directory")
                window = tk.Tk()
                window.withdraw()
                path = filedialog.askdirectory()
                f.write(path)
        os.chdir(path)
    except Exception as e:
        print("There was an issue with savegame path. Remove the savegamedir.txt and try again.")
        print(e)

    return

def backup():
    """
    Backup the save and move each backup slot forward one notch until backup 5.
    Savegame -> backup 1
    backup 1 -> backup 2
    backup 2 -> backup 3 and so on, the oldest version is removed.

    Parameters
    ----------
    None.

    Returns
    ----------
    None.
    """
    
    savedir = "3559"
    tempdir = "3559 - temp"

    for i in range(5, 0, -1):
        backupdir = backupdir = "3559 - backup " + str(i)
        prev_backup = "3559 - backup " + str(i - 1)

        if not os.path.exists(prev_backup) and (i != 1):
            continue
        if os.path.exists(backupdir):
            shutil.rmtree(backupdir)
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir)
        
        if i == 1:
            shutil.copytree(savedir, tempdir)
        else:
            shutil.copytree(prev_backup, tempdir)
            
        os.rename(tempdir, backupdir)

    input("Backup successful, press enter to exit.")


def restore():
    """
    Restore savegame from defined backup number.

    Parameters
    ----------
    None.

    Returns
    ----------
    None.
    """
    
    n_backups = len([x for x in os.listdir() if x.startswith("3559 - backup")])

    if n_backups == 0:
        input("No backups found. Press enter to exit.")

    while True:
        inp = input("Which save to restore (1-{})? ".format(n_backups))
        backupdir = backupdir = "3559 - backup " + inp

        if os.path.exists(backupdir):
            break
        else:
            print("Invalid backup number.")    

    if os.path.exists("3559"):
        shutil.rmtree("3559")
    shutil.copytree(backupdir, "3559")

    input("Savefiles successfully restored from backup {}, press enter to exit.".format(inp))

def interface():
    """
    Run the command line interface for the program.

    Parameters
    ----------
    None.

    Returns
    ----------
    None.
    """

    while True:
        print("Press B to backup or R to restore your Ghost Recon Wildlands savefile.")
        input_char = msvcrt.getch().decode()
        
        if input_char.lower() == "b":
            print("Confirm save BACKUP by pressing Y or return with any key.")
            if msvcrt.getch().decode().lower() == 'y':
                backup()
                break
            else:
                print("Savefile not backed up.")
                continue
        
        elif input_char.lower() == "r":
            print("Confirm save RESTORE by typing Y or return with any key.")
            if msvcrt.getch().decode().lower() == 'y':
                restore()
                break
            else:
                print("Savefile not restored.")
                continue
        else:
            print("Invalid option.")

if __name__ == "__main__":
    check_dir()
    interface()