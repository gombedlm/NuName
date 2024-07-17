# NuName Discord Bot

## Table of Contents
- [Setup](#script-setup)
    - [Dedicated-Setup(Linux-Server)](#dedicated-server-setuplinux-server)
    - [Non-Dedicated-Setup(Local-Desktop)](#non-dedicated-setup-local-desktop)
- [Connecting to your Server](#connecting-to-a-discord-server)
    - [Create-Profile](#creating-your-bots-discord-profile)
    - [Adding-Permissions](#adding-scopes-and-giving-it-permissions)
- [Updating-Your-Enviorment](#get-your-credentials-and-update-your-enviorment-file)
## Script Setup

### Non Dedicated Setup (Local-Desktop)

### Dependencies
**> WARNING: Python 3.9 SPECIFICALLY IS REQUIRED**
 Make sure you have python 3.9 EXACTLY. Ensure its installed before running the command if you have another python installation then you need to uninstall it or ensure you run it with pyhton 3.9 or you will end up with an installation that does not work properly.

 > Im also using the packages discord.py for the bot integration. as well as python-dotenv for the bots security, so we arent giving out any bot tokens to anyone.

### Clone the repository
Open the command terminal
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

#### Running on Windows locally
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.

##### Windows Auto-Start Configuration
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

#### Running on Linux locally
1. Open command terminal and navigate to the root directory of the bot.
```bash
cd path/to/your/bot.py
```

2. Run the bot.
```bash
python bot.py
```
> if you dont mind restarting your bot everytime you restart your computer then thats it you can stop there,  otherwise follow the instructions below.


##### Linux Auto-Start Configuration
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
 
### Dedicated Server Setup(Linux-Server)
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


## Connecting to a Discord Server

### Creating your bots discord profile
1. Enter a name for your app, then press Create.
You'll see an Application ID and Interactions Endpoint URL, which we'll use a bit later in the guide.
> After you create your app, you'll land on the General Overview page of the app's settings where you can update basic information about your app like its description and icon. 

2. Getting your bot token
There's a Token section on the Bot page, which allows you to copy and reset your bot's token.

> Bot tokens are used to authorize API requests and carry your bot user's permissions, making them highly sensitive. Make sure to never share your token or check it into any kind of version control.

**Go ahead and copy the token, and store the token somewhere safe (like in a password manager)**

### Adding Scopes and Giving it Permissions
1. Adding scopes and permissions to your bot
Next (If needed) select a few scopes and permissions to request before installing the app.

- > When creating an app, scopes and permissions determine what your app can do and access in Discord servers.

- > Apps need approval from installing users to perform actions in Discord (like creating a slash command or fetching a list of server members). 

- > OAuth2 Scopes determine what data access and actions your app can take, granted on behalf of an installing or authenticating user.

- > Permissions are the granular permissions for your bot user, the same as other users in Discord have. They can be approved by the installing user or later updated within server settings or with permission overwrites.

Click on OAuth2 in the left sidebar, then select URL generator.
- > The URL generator creates an installation link based on the scopes and permissions you select for your app. You can use the link to install the app onto your own server, or share it with others so they can install it.


### Get your credentials and update your enviorment file
1. Generate your invite Link
Once you add scopes, you should see a URL that you can copy and use this in .

2. Copy your APP-ID

3. Copy your PUBLIC_KEY

4. Copy your DISCORD_TOKEN

5. Update your .env file

# License 
**This project is licensed under the MIT License. See the LICENSE file for details.**
