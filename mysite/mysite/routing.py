# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing


#ProtocolTypeRouter将首先检查连接类型，如果它是WebSocket(ws://或wss://),将连接到AuthMiddlewareStack
#在AuthMiddlewareStack 将填充的连接的范围与到当前认证用户，然后将连接到URLRouter
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})