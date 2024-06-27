# Harmonica Tab Bot
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This telegram bot finds the best harmonica (mouth harp) tabs for a given song:

- Compute the best tabs for a song for the following 10-holes harmonica layouts: `Diatonic Major`, `Natural Minor`, `Harmonic Minor`, `Lee Oskar® - Melody Maker™` and `Chromatic Harp (12 holes)`
- Convert song notes to harmonica tabs
- Find and save songs with bot commands
- Language support: German & English

## Installation

Obtain a token from [Telegram BotFather](https://core.telegram.org/bots/tutorial) and save it as `bot.token`. 
Install and launch the bot as follows:

```
python3 -m venv venv/
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 HarmonicaTabBot.py
```

## Commands

Please enter /start or /help to the bot in order to get the full command set:

```
Settings:
  o /layout - Set your Harp Layout
  o /config - Language & other Settings
  o /songbook - Set Songbook

Commands:
  o /list - List of your Songs
  o /get - Random Song
  o /add - Add Song
  o /delete - Delete Song
  o /dump - Dump Song Data

Help:
  o /help - Show help
  o /howto - How to convert Song Notes to Tabs
```

## Example

```
> list

List of your Songs:

 1. Drunken Sailor
 2. Jingle Bells
 3. Twinkle, Twinkle, Little Star
 4. The Wellerman


> drunken sailor

Drunken Sailor
Diatonic Major (Score: 100.0%)

  6    -6    -6    -6    -6    -6  
 -6    -4    -5    -6  
  6     6     6     6     6     6  
  6     4     5     6  
 -6    -6    -6    -6    -6    -6  
 -6    -7     7    -8  
  7    -6     6     5  
 -4    -4
```


