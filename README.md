# GhostBackup
Backup script for Ghost Recon Wildlands.

The program is a python script, which can either backup or restore your save.
This is especially useful with the Ghost mode, as the game is full of bugs which can get you killed easily and hence remove your save.

The backups are located in your Ubisoft savegame directory (by default `C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/savegames/<Uplay user ID>`)
and the amount of backups you allow are kept for you to restore a previous game state if, for example, you have created a backup while downed and the game has declared you dead prematurely.

The GRW savefiles are in folder `3559` by default and this script creates as many backups as you specify. In other words, after reaching your backup limit you should have the following directory structure in your savegame folder:

```
C:
└── Program Files (x86)
    └── Ubisoft
        └── Ubisoft Game Launcher
            └── savegames
                └── <Uplay user ID>
                    ├── 3559
                    ├── 3559-1
                    ├── 3559-2
                    ├── 3559-3
                    ├── 3559-4
                    ├── 3559-5
                    └── 3559-latest
                    
```

## Instructions for python
version 3.11.5
1. Download the python script
2. Run the script by double-clicking it or via command line `python GhostBackup.py`
3. Run the initial setup sequence. This will require you to close and reopen the script.
4. Open the program to auto backup at your set timed interval.
5. If restoring save, enter [r]. If you would like to backup from latest just press [enter] otherwise enter [s] to select the restore file.
6. Enter [p] if you would like to reset your environment variables for the program. Please note any bugs in the issues tab.

## Instructions for .exe
1. Download the exe file in the dist folder
2. Run the script by double-clicking
3. Run the initial setup sequence. This will require you to close and reopen the script.
4. Open the program to auto backup at your set timed interval.
5. If restoring save, enter [r]. If you would like to backup from latest just press [enter] otherwise enter [s] to select the restore file.
6. Enter [p] if you would like to reset your environment variables for the program. Please note any bugs in the issues tab.

### Disclaimer

This script has only been tested on Windows 10/11 and its functionality is not guaranteed for other operating systems.

I am not liable for any damage or lost savegames, but please do message me if you have any issues.
