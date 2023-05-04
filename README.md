## Config

**GamesPath** - specify a path where the game session logs will be saved. Default saves to the same location as .exe file in *Games* directory (enter without quotation marks)

**OpeningScanInterval** - interval of seconds after which the check if a game is open will occur

**ClosingScanInterval** - interval of seconds after which the check if tracked game is no longer open will occur

**GameExeNames** - file with names of game .exe files and their full names



## Build

pyinstaller --noconfirm --onefile --console --icon "icon path" ".py file path"