# roblox-external-esp

# Table of Contents
Intro
Features
how it works
requirments
installation
usage

# Intro
Some can say that this script is worse than other scripts; it is.if you dont know what this script is for, ignore all of this, look somewhere else. This can be hidden from recording software just by recording only the Roblox window, Many esp scripts are not able to hide esp from obs or any recording due to the fact that the esp uses PlayergGui or CoreGui to place the UI instead of a window placed above the client, or the executor doesnt support OBS hide.

# Features
OBS hide
screen record hide
external esp
renders tracers, the opponent(s) name, and a line to the position.

# How it works
1. The lua script checks for all players on screen, then uses WorldToScreenPoint() to convert the 3D position to the position onscreen.
2. The lua script stores the data into a JSON script.
3. The Python script iterates through the JSON data.
4. The Python script uses Tkinter to render everything.

# requirments
1. The newest version of Python
2. any executor with a file system
3. Run "pip install tkinter" into cmd.
4. executor placed on a thumbdrive, SSD, or any solid-state storage device (this script uses read and write heavily).

# installation
1. Drag all files and folders into the workspace of the executor.

# usage
1. Open "external esp render.py" in the workspace of the executor
2. Run the lua script.
3. enjoy
4. Give me a rep on V3rmillion: (https://v3rm.net/members/randoperson0.5755/)
5. Give me rep on WeAreDevs: (https://forum.wearedevs.net/profile?uid=93002)
6. Donate to my LTC wallet: LXimp7Vm38fBbbpyTWeZG16ZrbqVu74M81

