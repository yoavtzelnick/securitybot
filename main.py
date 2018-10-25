#!/usr/bin/env python
import logging
import os
from securitybot.bot import SecurityBot
from securitybot.chat.slack import Slack
from securitybot.tasker.sql_tasker import SQLTasker
from securitybot.sql import init_sql

DUO_INTEGRATION = os.environ.get("DUO_INTEGRATION", None)
DUO_SECRET = os.environ.get("DUO_SECRET", None)
DUO_ENDPOINT = os.environ.get("DUO_ENDPOINT", None)

if all(DUO_SECRET, DUO_ENDPOINT, DUO_INTEGRATION):
    from securitybot.auth.duo import DuoAuth as AuthService
    import duo_client
    auth_api = duo_client.Auth(
        ikey=DUO_INTEGRATION,
        skey=DUO_SECRET,
        host=DUO_ENDPOINT
    )
else:
    from securitybot.auth.dummy import DummyAuth as AuthService
    auth_api = None

CONFIG = {}
SLACK_KEY = 'slack_api_token'
REPORTING_CHANNEL = 'some_slack_channel_id'
ICON_URL = 'https://dl.dropboxusercontent.com/s/t01pwfrqzbz3gzu/securitybot.png'

def init():
    # Setup logging
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s %(levelname)s] %(message)s')
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('usllib3').setLevel(logging.WARNING)

def main():
    init()
    init_sql()

    # Create components needed for Securitybot

    auth_builder = lambda name: AuthService(auth_api, name)

    chat = Slack('securitybot', SLACK_KEY, ICON_URL)
    tasker = SQLTasker()

    sb = SecurityBot(chat, tasker, auth_builder, REPORTING_CHANNEL, 'config/bot.yaml')
    sb.run()

if __name__ == '__main__':
    main()
