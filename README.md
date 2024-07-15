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

1. Get a copy of the repository
```bash
git clone https://github.com/gombedlm/NuName.git
```

2. Navigate to the root directory of the repository
```bash
cd NuName-Discord-Bot
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
Once you finish the installation and ensureing that you have the correct dependencies.

1. You are going to need to get yourself a Discord Bot Token
Sign in and create a profile for your new bot. ----> https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications%2F
> Essentially you just need to create a profile for your bot that you are adding to the server, the script you are installing is its logic to communicate with the server.


## Running the bot Locally
So if you dont feel like setting up an entire server or just dont have one, you dont need to.
### Windows
1. If you completed the installation and Enviormental Variable setup steps above, run your bot.py.
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.

### Linux
1. If you completed the installation and Enviormental Variable setup steps above, run your bot.py.
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.

## Running the bot on a dedicated server
### Windows
### Linux