![lapzbot](http://i.imgur.com/Y86fweN.png)
### What is lapzbot?
lapzbot is a multi-purpose utility bot that I wrote for my discord server `osu! India`. Needless to say the functions I have created are designed keeping the osu crowd in mind. If you want to use this bot, go ahead and use it. I will try to keep it as updated as possible.

Join my [lapzbothelp Discord Server](https://discord.gg/0lzW6jSQESAO1HSU) to get latest updates/ help/ bugfixes etc on lapzbot.

### How to set it up?
1. Install [Python 3.5.1](https://www.python.org/downloads/)
    * Make sure you select this option in the Python install: **Install launchers for all user** and **Add Python 3.5 to PATH**. After that do **Install Now**. (*Don't click on Customize installation*) 
2. Install [Git](https://git-scm.com/download/win)
3. Install [PyYAML 3.11](http://pyyaml.org/wiki/PyYAML) 
4. Download the **async version** of [Discord.py](https://github.com/Rapptz/discord.py/tree/async)
    * Alternatively, open comamnd prompt and type `pip install git+https://github.com/Rapptz/discord.py@async` . P.S. This requires Python and Git to be installed first. So complete steps 1 and 2 before doing this.
5. Download the bot by clicking on **Download ZIP** near the top right hand side of this site
6. Unzip the bot
7. Goto the bot folder once you have unzipped. There are 2 folders inside :- **audio_library** and **configuration**
    * **audio_library** :- Place you mp3 files here. (Try not to put a huge amounts of songs inside this as currently it processes all the songs while loading to voice channel.)
    * **configuration** :- Inside this there is a file called `config.yaml`. Open this with a text editor. I recommend using [Notepad ++](https://notepad-plus-plus.org/download/v6.8.8.html). **Edit the values only. Don't change anything else.** [Check the wiki](https://github.com/lapoozza/lapzbot/wiki) for detailed information on how to edit the config.yaml file. Save the config.yaml file.
8. Double-click the `lapzbot.py` file. (In case that doesnt work, right click 'lapzbot.py' and open it with IDLE. Then from IDLE, press `F5` )


### Command list
* `!help` :- Displays a list of commands that you can use.
* `!stats <username>` :- Displays username, PP, playcount and accuracy using the osu! API. Make sure that if your username contains more than 2 word, user underscore to separate the words. Ex :- @lapzbot stats John_Smith
* `!top <username>` :- Displays the top 5 plays of the user. Currently experimental. Refer to above on how to format your username.
* `!guess` :- Starts a number guessing game
* `!quiz` :- Asks a random question

### Music Player functions
* `!load` :- Hooks the bot to the voice channel you are currently joines. (*Remember to join a voice channel first before using this command*). Once it hooks itself, it will display a list of mp3 files inside the **audio_library** folder against a code that can be used to play the file.
* `!play <id>` :- Play a song represented by that id. (*In order to play a new song, the current song must finish playing or alternatively you can use* `!stop`)
* `!pause` :- Pauses the current song
* `!resume` :- Resumes the current song that was paused
* `!stop` :- Stops playing the current song
* `!playlist` :- Displays the playlist.

### Emoticon list
* `!kappa`
* `!feelsgoodman`
* `!feelsbadman`
* `!lapz`
