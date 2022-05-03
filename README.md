# GhostBackup
Backup script for Ghost Recon Wildlands.

The program is a python script, which can either backup or restore your save.
This is especially useful with the Ghost mode, as the game is full of bugs which can get you killed easily and hence remove your save.

The backups are located in your savegame directory (by default `C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/savegames/d94c6c98-13b0-4a68-b6cb-530a1af44cbf`)
and up to five backups are kept allowing you to restore a previous game state if, for example, you have created a backup while downed and the game has declared you dead prematurely.

The GRW savefiles are in folder `3559` and this script creates up to five backups. In other words, after five backups you should have the following directory structure in your savegame folder:

```
C:
└── Program Files (x86)
    └── Ubisoft
        └── Ubisoft Game Launcher
            └── savegames
                └── d94c6c98-13b0-4a68-b6cb-530a1af44cbf
                    ├── 3559
                    ├── 3559 - backup 1
                    ├── 3559 - backup 2
                    ├── 3559 - backup 3
                    ├── 3559 - backup 4
                    └── 3559 - backup 5
```

## Instructions

1. Download the python script
2. Run the script by double-clicking it or via command line `python GhostBackup.py`
3. Press B to backup your save or R to restore it
4. Press Y to confirm
5. If restoring save, select a save number by typing the number (1-5) 

### Disclaimer

This script has only been tested on Windows 10 and its functionality is not guaranteed for other operating systems.

I am not liable for any damage or lost savegames, but please do message me if you have any issues.
