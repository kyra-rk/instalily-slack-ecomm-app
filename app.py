import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    # contains array of blocks (building components of a Slack message eg. text, images, datepickers)
    # here, app will respond w action block that includes a button
    # text is a fallback for notifications and accessibility
    # button is an accessory object -- action_id is a unique identifier
    say(
        blocks=[
            {
                "type":"section",
                "text":{"type":"mrkdwn", "text":f"Hey there<@{message['user']}>!"},
                "accessory":{
                    "type": "button",
                    "text": {"type":"plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

# sets button to listen for th action_id specified ("button_click")
@app.action("button_click")
def action_button_click(body, ack, say):
    # acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button.")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()