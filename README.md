preview image can be seen here (https://v3rm.net/threads/free-release-open-source-roblox-external-tracer-esp-obs-hide-renders-externally-works-with-any-exec.9702/)

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
1. Windows 10/11
2. The newest version of Python
3. any executor with a file system
4. Run "pip install tk" into cmd. more about tkinter (https://docs.python.org/id/3.12/library/tkinter.html)
5. Run "pip install pywin32" into cmd. more about pywin32 (https://github.com/mhammond/pywin32)
6. Run "pip install dearpygui" into cmd. more about dearpygui (https://github.com/hoffstadt/DearPyGui)
7. Download Pymeow zip (https://github.com/qb-0/pyMeow)
8. rename the zip file to pyMeow (dont remove .zip)
9. right click where the zip file is located ( not the file itself)
10. open cmd/powershell/Terminal in right click menu
11. Run "pip install pyMeow.zip"
12. Decent gpu. This script may be gpu intensive and very unoptimized.

# installation
1. download  zip
2. unzip
3. Drag all unzipped files and folders into the workspace of the executor.

# usage instructions
1. Copy everything in the lua script, paste into any exec (thats decent), and run
2. Run "external esp render.py" in the workspace of the executor
3. enjoy

#support me
join my discord server: [discord.gg/pm5Fj6tjv2](https://discord.com/invite/pm5Fj6tjv2)

rep me on V3rmillion: (https://v3rm.net/members/randoperson0.5755/) (optional) 

rep me on WeAreDevs: (https://forum.wearedevs.net/profile?uid=93002) (optional) 

Donate to my LTC wallet: LXimp7Vm38fBbbpyTWeZG16ZrbqVu74M81 (optional, this will be used mainly towards my subscriptions for my executor)

