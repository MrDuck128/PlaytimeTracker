## Usage

- Download *Playtime Tracker.exe*, *Session Tracker.exe*, *gamesExeNames.json* and GameIcons folder


## Playtime Tracker

- Launch **Playtime Tracker.exe** to see games and their respective playtimes

- To add pictures to game listings, put a .png file with the game name (can be custom but must match the game name in *gamesExeNames.json*) in the folder named GameIcons (GameIcons must be in the same directory as the executable)


## Session Tracker

- Launch **Session Tracker.exe**, then launch your game of choice, the tracker should say that it started tracking and list the game. After you close the game, tracker will stop by itself depending on the *ClosingScanInterval*. It will display the save location directory and the session playtime

- If the tracker doesn't recognise your game, add the game name into the **gamesExeNames.json** like so: "gameExe.exe": "GameName (can be whatever)"

- Run **gameNameOrder.py** to sort game names in *gamesExeNames.json* alphabetically

- You can edit the config for more options (check below). If there is no config file *Session Tracker.exe* will create one with default values on launch


## Config

**GamesPath** - specify a path where the game session logs will be saved. Default saves to the same location as .exe file in *Games* directory (enter without quotation marks)

**OpeningScanInterval** - interval of seconds after which the check if a game is open will occur

**ClosingScanInterval** - interval of seconds after which the check if tracked game is no longer open will occur

**GameExeNames** - file with names of game .exe files and their full names


## Build

pyinstaller --noconfirm --onefile --console --icon "icon path" ".py file path"