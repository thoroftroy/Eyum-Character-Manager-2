# Eyum Character Manager 2
A utility program for managing characacters for the TTRPG the World of Eyum


This program is a beta release, it does not have most of the features required for leveling, however it can be used for basic character management. Keep in mind, this program is not meant to replace the character sheet, more to make it slightly easier to manage. Some features (like abilities, languages, profiencies, and skills) aren't really implimented into this.

The structure of the program is as follows. The left side of the screen is the skill tree (NOT YET FINISHED) and the right side of the screen contains the control panel and the character information panel. The character information panel shows you all of the information currently saved about your character while the control panel lets you save and load other characters as well as roll dice easily in the program. 

# Install Inscructions
Simply go to the realeases page and download all 3 of the main files, the .sh the .86x and the .pck files respectivly. All files must be present in the same folder for the program to work. 
Save files are saved in /home/USERNAME/.local/share/godot/app_userdata/ECM2/SaveFiles. 
You may have to chmod +x the sh and appimage files for the program to work.

# Web version
The idea behind this is that any device *should* be able to open and run EYM2. However, this feature is not yet working at all, so don't bother to download the web version. The web version is only uploaded at the moment for archiving purposes. 

# OS Support
Will this ever support windows?
  No probably not

Does this work on every Linux OS?
  Maybe? I haven't tested it on everything but so far it works great.

Will it support X hardware?
  The likley answer is yes, unless your computer is really old. I tried running it on an old windows xp era laptop and it couldn't do it at all beacuse it didn't support openGl 3, so I switched the renderer to Vulkan and it launched but creating save files seems to crash it. 

Good luck and have fun!
