import os
import time
import sys
from slackclient import SlackClient
from daemonize import Daemonize

daemon = sys.argv[1] == "-d"
app_name = "bot_app"

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

def postMsg(msg, channel="#wass-memo"):
    sc.api_call(
    "chat.postMessage",
    channel=channel,
    text=msg
    )

def responseMsg(rtm, msg):
    postMsg(msg, channel=rtm["channel"])

def response(rtm):
    if rtm["text"].startswith("Hey"):
        responseMsg(rtm, "hello")

def main():
    if sc.rtm_connect():
        while True:
            for rtm in sc.rtm_read():
                if rtm["type"] == "message":
                    response(rtm)
            time.sleep(1)
    else:
        print("Connection Failed")

if daemon:
    print("Deamon Mode")
    
    d = Daemonize(app=app_name, pid=app_name+".pid",
                       action=main, keep_fds=keep_fds)
    d.start()
else:
    main()