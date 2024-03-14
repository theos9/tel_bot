# from pyrogram import Client
from pyromod import Client
plugins=dict(root="plugins")


app= Client(name="shoping_bot",
            api_id=None,
            plugins=plugins,
            api_hash=None,
            bot_token="6934645347:AAG-wRCvVg3JXJ71NG2eh3ysWUqE4FOtw_I")



app.run()