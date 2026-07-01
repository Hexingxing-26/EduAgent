from api.conversation_router import router as conv_router
from api.portrait_router import router as portrait_router
from api.v1.chat_stream_router import router as chat_stream_router

all_v1_routers = [conv_router, portrait_router, chat_stream_router]