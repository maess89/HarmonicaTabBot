# Harmonica Tab Bot
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This Telegram bot finds the best harmonica tabs for a given song. Key features:

- Supports 10-hole harmonica layouts: Diatonic Major, Natural Minor, Harmonic Minor, Lee Oskar® - Melody Maker™, and Chromatic Harp (12 holes).
- Converts sheet music notes into harmonica tabs.
- Finds the best harmonica layout for a given song and considers your proficiency at bending notes.
- Allows you to manage songs using bot commands.
- Available in German and English.

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
  o /layout - Set your harmonica
  o /config - Bot settings & language

Commands:
  o /list - List of your songs
  o /get - Random song
  o /add - Add song
  o /delete - Delete song
  o /dump - Dump song Data

Help:
  o /help - Show help
  o /howto - How to convert song notes to tabs
```

## Example

Simply type in some notes in order to find the best tabs for your harp layout (`/layout`), e.g. Tetris:

```
> E2 B C2 D2 C2 B A | A C2 E2 D2 C2 B | C2 D2 E2 | C2 A A

Your Song
Diatonic Major (Score: 100.0%)
-6  5 -5  6 -5  5 -4 | -4 -5 -6  6 -5  5 | -5  6 -6 | -5 -4 -4
```

You can list your songs and get a specific one as follows:

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

 -6    -6    -6    -6    -6    -6  
 -6    -4    -5    -6  
  6     6     6     6     6     6  
  6     4     5     6  
 -6    -6    -6    -6    -6    -6  
 -6    -7     7    -8  
  7    -6     6     5  
 -4    -4
```