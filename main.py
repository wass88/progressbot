import os
import os.path
import time
import sys
import logging
from slackclient import SlackClient
from daemonize import Daemonize

app_name = "bot_app"
pid = app_name+".pid"

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

logger = logging.getLogger(__name__)
d = Daemonize(app=app_name, pid=app_name+".pid", action=main, logger=logger)

daemon = len(sys.argv) >= 2 and sys.argv[1] == "-d"
kill = len(sys.argv) >= 2 and sys.argv[1] == "-k"
restart = len(sys.argv) >= 2 and sys.argv[1] == "-r"

if len(sys.argv) < 2:
    print("NON Daemon Mode")
    main()
else:
    if sys.argv[1] == "stop":
        d.exit()
    elif sys.argv[1] == "start":
        print("Daemon Mode: pid =", pid)
        d.start()
    else:
        sys.stderr.write("Unknown Option")
