# NuName Discord Bot

## Table of Contents
- [Setup](#Setup)
- [Local Configuration](#LocalConfiguration)
- [Dedicated Configuration](#DedicatedConfiguration)
- [Adding your Bot](#adding-the-bot-to-your-server)
- [Windows Configuration](#WindowsConfiguration)
- [Linux Configuration](#LinuxConfiguration)
- [Contributing](#contributing)
- [License](#license)

# Setup

## Local Setup

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
> Go to the Discord Developer Portal and click "New Application" , name it whatever youd like, then click "Bot" on the left hand menu and select your new bot. Then click "Reset Token" and copy the one that pops up, this is your Bot Token.

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

### Running on Windows
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.

#### Windows Auto-Start Configuration
1. Using Task Scheduler on Windows
    Press Win + R to open the Run dialog.
    - Type taskschd.msc and press Enter to open Task Scheduler.
    - Click on "Create Task..." on the right-hand side under the "Actions" pane.


2. General Tab:
    Name your task (e.g., "NuName Discord Bot").
    - (Optional) provide a description.
    - (Required) Select "Run whether user is logged on or not."
    - (Required) Check "Run with highest privileges."

3. Triggers Tab:
    Click "New..." to create a new trigger.
    - In the "New Trigger" window, select "At startup" from the "Begin the task" dropdown.
    Click "OK."

4. Actions Tab:
    Click "New..." to create a new action.
    - In the "New Action" window, set the "Action" dropdown to "Start a program."
    - In the "Program/script" field, enter the path to your Python executable (e.g., C:\Path\To\Python\python.exe).
    - In the "Add arguments (optional)" field, enter the path to your bot script (e.g., C:\Path\To\NuName-Discord-Bot\bot.py).

5. Conditions Tab:
    Adjust any other conditions as needed.
    - Uncheck "Start the task only if the computer is on AC power" if you want the bot to run on battery power as well (Only for laptops).


6. Settings Tab:
    - Check "Allow task to be run on demand."
    - Check "Run task as soon as possible after a scheduled start is missed."



7. Finish:
    - Click "OK" to create the task.
    > **You will be prompted to enter your Windows account password to save the task.**

### Running on Linux
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.


#### Linux Auto-Start Configuration
1. Create a systemd service file in the /etc/systemd directory:
```bash
sudo nano /etc/systemd/system/nuname-discord-bot.service
```
2. Paste the following Configuration into the file:
```bash
[Unit]
Description=NuName-Discord-Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/NuName-Discord-Bot
ExecStart=/usr/bin/python3 /path/to/NuName-Discord-Bot/bot.py
Restart=on-failure
User=your_linux_username

[Install]
WantedBy=multi-user.target
```

3. Replace /path/to/NuName-Discord-Bot, /usr/bin/python3, your_linux_username with your actual paths and username information.
```bash
WorkingDirectory=/path/to/NuName-Discord-Bot
ExecStart=/usr/bin/python3 /path/to/NuName-Discord-Bot/bot.py
User=your_linux_username
```
**WARNING:**Change these only do not alter any other info unless you know what you are changing.

4. Save the file ('Ctl + x' then 'Y', then 'Enter')

5. Start the services and enable it (so it starts on boot)
```bash
sudo systemctl start nuname-discord-bot
sudo systemctl enable nuname-discord-bot
```

6. Check its status to make sure its not being stupid
```bash
sudo systemctl status nuname-discord-bot
```

## Setup on Dedicated Server
This is a guide for if you already have a dedicated server running youd like to run this on.
1. Prepare the server enviorment 
    make sure that your enviorment is up to date
```bash
sudo apt update
```
2. Ensure your server has python 3.9 installed
```bash
sudo apt-get install python3.9 
```
3. Ensure your server has git installed 
```bash 
sudo apt-get install git
```

4. Clone the repository:
Connect to your server via ssh or any remote access method and enter the following into the command line.
```bash
git clone https://github.com/gombedlm/NuName.git
cd NuName
```
5. Install Dependencies:
```bash
pip install -r requirements.txt
```
6. Configure Environmental Variables:
Ensure that '.env' file is properly configured with the necessary environment variables particularlly 'DISCORD_TOKEN' where you will store your bots token (so no bad actors will hack into your servers bot)
```bash
DISCORD_TOKEN=your_discord_bot_token_here
```
7. Start the bot
Run the script in your server enviorment
```bash
python bot.py
```
8. Ensure connectivity
This will start your discord bot on the server that the token is registered to. Ensure that you see the log messages indicating the bot is ready - "NuName bot is ready".


# Adding the bot to your discord server

### Local Configuration
1. Generate your invite link:
    - Ensure your bot is running either locally on your machine (either Windows or Linux) or on a dedicated server.
    - Open your web browser and go to the Discord Developer Portal.
    - Navigate to your Discord Developer Portal, find your bot app and select the "OAuth2" tab from the left sidebar.

2. OAuth2 Configuration:
    - In the "OAuth2 URL Generator" section, under "OAuth2 URL Generator," select the scopes needed for your bot (bot for adding as a bot) and the permissions required
    - Copy the generated URL.

3. Invite to Server:
    - Paste the copied URL into your web browser's address bar and press Enter.
    - Select the server you want to add the bot to from the dropdown list.
    - Click "Authorize" and complete any CAPTCHA prompts if necessary.
4. Verify:
After authorization, your bot will join the selected server.

### Dedicated Server Configuration
1. Generate Invite Link:
    - Ensure your bot is deployed and running on your dedicated server.
    - Follow steps 1 and 2 from the Local Install section to generate an OAuth2 URL with the appropriate permissions.

2. Invite to Server:
    - Copy the generated OAuth2 URL and paste it into your web browser's address bar.
    - Choose the server where you want to add the bot and authorize it by clicking "Authorize."
**WARNING: Make sure you enable, "REQUIRES OAUTH2 CODE GRANT", and all "Privileged Gateway Intents"**

3. Verify:
After authorization, your bot will join the selected server.







# License 
**This project is licensed under the MIT License. See the LICENSE file for details.**
