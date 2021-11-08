Discord + Telegram Twitter Bot
============
[![https://discord.gg/EstHC38D](https://img.shields.io/badge/%F0%9F%92%AC_Discord-Dyhaz%20Bot._Group-blue.svg)](https://discord.gg/EstHC38D)


Description
------------

A Discord + Telegram Bot based on Tweepy.

Project Structure
------------
```
discord_bot
│   README.md
│   main.py
│   .env
│   alembic.ini
│   requirements.txt  
│
└───alembic
│   │   env.py
│   │   README
│   │
│   └───versions
│       │   a308fc57244b_create_coupon_table.py
│       │   ...
│   
└───source
    │   bot_commands.py
    │   discord
    │   helpers
    │   models
    │   telegram
```

Bot Commands
------------
<table>
  <thead>
    <tr>
      <td><strong>Name</strong></td>
      <td><strong>Description</strong></td>
      <td><strong>Usage</strong></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>!info</td>
      <td>Fetch latest info</td>
      <td>Send latest likes from twitter users</td>
    </tr>
    <tr>
      <td>!invite</td>
      <td>Invite bot to your channel</td>
      <td>Send invitation link via DM</td>
    </tr>
    <tr>
      <td>!version</td>
      <td>Show version</td>
      <td>Show bot version</td>
    </tr>
  </tbody>
</table>

Installation
------------
Edit and rename .env.example to .env according to your bot configuration and then execute:
1.  `pip install -r requirements.txt`
2.  `main.py -b [discord/telegram]`