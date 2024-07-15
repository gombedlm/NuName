# NuName Discord Bot

## Table of Contents
- [Setup](#setup)
- [Running the Bot Locally](#running-the-bot-locally)
- [Running the bot on a Dedicated Server](running-on-a-dedicated-server)
- [Running in the Background](#running-in-the-background)
- [Adding the Bot to Your Server](#adding-the-bot-to-your-server)
- [Contributing](#contributing)
- [License](#license)

# Setup
## Running the Bot Locally

### Dependencies
**> WARNING: Python 3.9 SPECIFICALLY IS REQUIRED**
 Make sure you have python 3.9 EXACTLY. Ensure its installed before running the command if you have another python installation then you need to uninstall it or ensure you run it with pyhton 3.9 or you will end up with an installation that does not work properly.

 > Im also using the packages discord.py for the bot integration. as well as python-dotenv for the bots security, so we arent giving out any bot tokens to anyone.

### Clone the repository
1. Open the command terminal
2. Clone the repository
```bash
git clone https://github.com/gombedlm/NuName.git
```

3. Navigate to the root directory of the repository
```bash
cd NuName-Discord-Bot
```

### Installation
1. Open the command terminal 

2. Install the requirements from the requirements.txt
```bash
pip install -r requirements.txt
```

3. Ensure that the following dependencies were installed.
```bash
discord.py
python-dotenv
```

### Environment Variables
Once you finish the installation and ensureing that you have the correct dependencies.

1. You are going to need to get yourself a Discord Bot Token to make this whole thing work:
Sign in and create a profile for your new bot. ----> https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications%2F
> Essentially you just need to create a profile for your bot that you are adding to the server, the script you are installing is its logic to communicate with the server.
2. Navigate to the root directory using:
```bash
cd NuName-Discord-Bot
```

3. Once you have your bot token find the '.env' file in your root directory:
Replace the value in the variable below with your bot token.
```bash
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
```

## Running the bot
So if you dont feel like setting up an entire server or just dont have one, you dont need to.
### Windows
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.


### Linux
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.

## Running the bot on a dedicated server
### Windows
### Linux

##