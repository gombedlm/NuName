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
## Local Configuration

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

### Running the bot locally
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

#### Setup the bot to run automatically
1. Using Task Scheduler on Windows
Press Win + R to open the Run dialog.
Type taskschd.msc and press Enter to open Task Scheduler.
Click on "Create Task..." on the right-hand side under the "Actions" pane.


2. General Tab:

Name your task (e.g., "NuName Discord Bot").
(Optional) provide a description.
(Required) Select "Run whether user is logged on or not."
(Required) Check "Run with highest privileges."

3. Triggers Tab:

Click "New..." to create a new trigger.
In the "New Trigger" window, select "At startup" from the "Begin the task" dropdown.
Click "OK."

4. Actions Tab:

Click "New..." to create a new action.
In the "New Action" window, set the "Action" dropdown to "Start a program."
In the "Program/script" field, enter the path to your Python executable (e.g., C:\Path\To\Python\python.exe).
In the "Add arguments (optional)" field, enter the path to your bot script (e.g., C:\Path\To\NuName-Discord-Bot\bot.py).

5. Conditions Tab:

Uncheck "Start the task only if the computer is on AC power" if you want the bot to run on battery power as well (Only for laptops).
Adjust any other conditions as needed.

6. Settings Tab:

Check "Allow task to be run on demand."
Check "Run task as soon as possible after a scheduled start is missed."
Optionally, adjust any other settings according to your preferences.


7. Finish:

Click "OK" to create the task.
You will be prompted to enter your Windows account password to save the task.

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

## Dedicated Server Configuration
If you have a server configured or have an extra linux system that can be used to connect your bot use this configuration.

### Windows
### Linux

# Contributing
Contributions are welcome, this is simply a rough template for the logic of a very simple bot for discord and it still has lots of potential.

# License 
