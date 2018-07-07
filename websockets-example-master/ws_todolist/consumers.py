from channels import Group
from ws_todolist.models import Item
from django.core import serializers

# Connected to websocket.connect
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("todolist").add(message.reply_channel)

    response_text = serializers.serialize('json', Item.objects.all())
    message.reply_channel.send({
        "text": response_text,
    })

# Could be connected to websocket.receive
# def ws_message(message):
#     Group("todolist").send({
#         "text": "blah, blah, blah",
#     })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("todolist").discard(message.reply_channel)
