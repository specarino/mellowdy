from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope
import os
from dotenv import load_dotenv

load_dotenv()


APP_ID = os.getenv("TW_APP_ID")
APP_SECRET = os.getenv("TW_APP_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


async def authenticate():
    print("Waiting on Twitch authentication...")
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, USER_SCOPE)
    await helper.bind()
    print("Twitch authenticated!")
    await twitch.close()
