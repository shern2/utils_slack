'''
Slack utilities
'''

from typing import Union, Dict, Any
from pathlib import Path
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

__all__ = ['MySlackApp']

class MySlackApp:
    '''Slack app
    (Need to setup the Slack App, bot, bot token, register the bot scope, install the app in Slack workspace, install app in the channel, etc.)
    '''

    def __init__(self, tkn:str, channel_id:str, slack_id:str):
        '''Setups a client with Slack Bot API token `tkn` that has the scope to write to the channel 
        of ID `channel_id`.
        `slack_id` is your target slack ID to @mention yourself if required.
        '''
        self.client = WebClient(token=tkn)
        self.channel = channel_id
        self.slack_id = slack_id
    
    def slack_me(self, msg:str, mention:bool=False):
        '''Sends the slack message to `self.channel`. Throws a `SlackApiError` if failed.
        If `mention` is True, includes a @mention at the end of the message
        '''

        self.client.chat_postMessage(
            channel=self.channel,
            text=(
                msg + f'\n<@{self.slack_id}>' if mention else msg
            ),
        )
        
    def upload(
        self,
        file:Path,
        title:str='',
        initial_comment:str="Here is the file:",
        ret_resp:bool=False,
    ) -> Union[Any,None]:
        '''Upload a file to the `self.channel`, with the `title` and `initial_comment` as described by Slack API docs:
        https://api.slack.com/methods/files.upload
        
        If `ret_resp` is True, returns the corresponding response.

        NOTE: requires Slack permissions at least: "files:write"
        '''
        resp = self.client.files_upload(
            channels=self.channel,
            title=title if title else file.name,
            file=file.as_posix(),
            initial_comment=initial_comment,
        )
        if ret_resp:
            return resp


    def rm(self, file_id:str):
        '''Deletes/Removes the file of `file_id` from the `self.channel`.
        '''
        resp = self.client.files_delete(channels=self.channel, file=file_id)


    def ls(self, ret_raw:bool=False) -> Union[Any,Dict]:
        '''Lists the files in the workspace (NOTE: 1st page only!).
        If `ret_raw` is True, returns the raw Slack response.
        '''
        resp = self.client.files_list(channel=self.channel)
        if ret_raw:
            return resp
        return resp.data['files']