from channels.routing import route
from ws_todolist.consumers import ws_add, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add),
#   route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
 
