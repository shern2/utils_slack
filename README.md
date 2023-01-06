Slack utilities

> :warning: This repo is solely for my own use. Use at your own risk.


# Installation

Recommend to use `dotenv` to store your tokens etc. (Install via e.g. `pip install python-dotenv==0.21.0`)

```bash
pip install --force-reinstall --no-cache https://github.com/shern2/utils_slack/archive/refs/tags/v1.zip
```

# Getting Started

```py
from dotenv import dotenv_values
env_vars = dotenv_values('proj.env') # load your env variables for the file

from utils_slack import MySlackApp
class MyNotif:
    '''My notifier (using Slack)'''
    tkn = env_vars.get('slack_tkn')
    if tkn is None:
        print('WARNING: Unable to use `MyNotif` as token not found')
    else:
        app = MySlackApp(tkn,env_vars['slack_channel'], env_vars['slack_id'])
        
        slack_me = app.slack_me


MyNotif.slack_me('I work smooth like butter :)', mention=True) 
```