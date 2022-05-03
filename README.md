# GhostBackup
Backup script for Ghost Recon Wildlands.

The program is a python script, which can either backup or restore your save.
This is especially useful with the Ghost mode, as the game is full of bugs which can get you killed easily and hence remove your save.
The backups are located in your savegame directory (by default `C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/savegames/d94c6c98-13b0-4a68-b6cb-530a1af44cbf`)
and up to five backups are kept allowing you to restore a previous game state if, for example, you have created a backup while downed and the game has declared you dead prematurely.

## Instructions

1. Download the python script
2. Run the script by double-clicking it or via command line `python GhostBackup.py`
3. Press B to backup your save or R to restore it
4. Press Y to confirm
5. If restoring save, select a save number by typing the number (1-5) 
