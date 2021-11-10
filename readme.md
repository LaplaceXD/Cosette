# Cosette
![Last Update](https://img.shields.io/github/last-commit/LaplaceXD/Cosette?color=blue&label=Last%20Update) ![Activity](https://img.shields.io/badge/Activity-Maintaining-blueviolet)

Cosette is a simple music bot that I created to learn `python` and to satiate my curiosity on how to create `discord bots`. The bot can be used through the `!` command prefix.

## How to add to Discord?
1. Go to do this [link](https://discord.com/oauth2/authorize?client_id=893906543177768961&permissions=8&scope=bot).
2. Select the server where you want the bot to reside.
3. Grant authorization.
4. Type `!ping` to test whether the bot is now in your discord.
5. ...
6. Profit.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies of this project.

```bash
pip install -U discord.py pynacl youtube-dl dacite Flask
```

You also need FFmpeg in your PATH environment variable or the FFmpeg.exe binary in your bot's directory on Windows.

Alternatively, you can also fork my [repl.it](https://replit.com/@LaplaceXD/MusicPlayer) where I am hosting the bot.

## Usage
*I have been too busy, I'll update this once I have properly documented the bot.*

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Roadmap
```
IMPORTANT: Refactor first before finishing

URGENT: Separate funbot from musicbot so you can add nhentai feed on funbot
URGENT: Decouple music and youtubeDL and create a service for youtubeDL instead of creating a source

CURRENTLY:
- Adding description to bot how many guilds its playing at
- Adding !help
- Implement a logger
- Add volume
- Adding !skipplay
- Adding !clear
- Adding !stop
- Learn what discord.intents are and start restricting the permissions of the bot
- slowly document bot

Refactoring:
- Handle Errors and looking for other sources on youtube DL
- Add looping playlist

To be implemented:
- add !autoplay [on|off|status] feature which plays the next recommended video of youtube
- next / skip // add numbers for this one to instantly skip
- Bot should not activate commands that are different from the channel that it was instantiated

- add emoji control support
- use db to save playlist using !saveasplaylist [name]
- !playlist [name] to play a set of songs
- playlist support from youtube
- spotify and other music streaming support

VERY FAR FROM THE PIPELINE:
skipto - to skip to certain song in the queue and it deletes the prior songs
fastforward - to ff the song by providing time in seconds
rewind - opposite of fastforward
move - move a song up or down in the queue
seek - to move to certain timestamp in rhe current playing song
loopqueue - to replay the queue after it plays the last song
```

## Acknowledgement
- [FreeCodeCamp - How to Code a Discord Bot](https://www.youtube.com/watch?v=7rU_KyudGBY) taught me how to keep the bot alive in my repl.
- [Max A - How to make a music bot like rhythm](https://www.youtube.com/watch?v=jHZlvRr9KxM&t=321) taught me the basics on how to set up a music bot in repl and how to make use of `discord.py` to create one.
- [vbe0201 - music_bot_example](https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d) taught me the more advanced stuff on creating a music bot, such as Asyncio, event loops, and so on.
- [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html)

## License
[MIT License](https://raw.githubusercontent.com/LaplaceXD/Cosette/master/LICENSE)
```
Copyright (c) 2021 Jonh Alexis Buot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```