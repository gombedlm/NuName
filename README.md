# NuName Discord Bot

## Table of Contents
- [Setup](#setup)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Clone the Repository](#clone-the-repository)
- [Running the Bot](#running-the-bot)
  - [Locally on Windows](#locally-on-windows)
  - [Locally on Linux](#locally-on-linux)
- [Running in the Background](#running-in-the-background)
  - [Using Task Scheduler on Windows](#using-task-scheduler-on-windows)
  - [Using Systemd on Linux](#using-systemd-on-linux)
- [Adding the Bot to Your Server](#adding-the-bot-to-your-server)
- [Contributing](#contributing)
- [License](#license)

## Setup

### Dependencies
**> WARNING: Python 3.9 SPECIFICALLY IS REQUIRED**
 Make sure you have python 3.9 EXACTLY. Ensure its installed before running the command if you have another python installation then you need to uninstall it or ensure you run it with pyhton 3.9 or you will end up with an installation that does not work properly.

 > Im also using the packages discord.py for the bot integration. as well as python-dotenv for the bots security, so we arent giving out any bot tokens to anyone.

### Clone the repository
Open the command line (Linux & Windows) or Powershell (Windows Only) and run the following commands: 

Get a copy of the repository
```bash
git clone https://github.com/gombedlm/NuName.git
```

### Installation
With that same command line open run the following commands: 

1. Install the requirements from the requirements.txt
```bash
pip install -r requirements.txt
```

2. Ensure that the following dependencies were installed.
```bash
discord.py
python-dotenv
```

### Environment Variables
 When you finish the installation section, there will be a file in your root folder called '.env' that contains an line of code, shown below.
```bash
DISCORD_TOKEN=your-bot-token
```
1. Here you will need to replace the placeholder text with your actual bot token that you can find in your discord developer dashboard here when you create the bot for the server using the following (Just sign in and make a new bot profile) ---> https://discord.com/login?redirect_to=%2Fdevelopers

 > if you get stuck heres a step by step guide to getting your bot token with pictures :3 https://www.writebots.com/discord-bot-token/


## Running the bot Locally
So if you dont feel like setting up an entire server or just dont have one, you dont need to.
### Windows
1. If you completed the installation and Enviormental Variable setup steps above, run your bot.py.
> if you dont mind restarting you bot everytime you restart your server then thats it you can stop there, if you would like it to restart and run with your computer then follow the instructions below 
### Linux

## Running the bot on a dedicated server
### Windows
### Linux