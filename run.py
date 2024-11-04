from contextlib import asynccontextmanager
from fastapi import FastAPI
from chatdollkit_aituber import ChatdollKitClient, get_router as get_client_router
from chatdollkit_aituber.comment import CommentMonitorManager
from chatdollkit_aituber.comment_api import get_router as get_comment_router

client = ChatdollKitClient(host="localhost", port=8888)

def process_comment(pytchat_comment):
    client.process_dialog(f"@{pytchat_comment.author.name}:{pytchat_comment.message}")

comment_monitor_manager = CommentMonitorManager(process_comment)

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    yield
    comment_monitor_manager.stop()


app = FastAPI(lifespan=lifespan, title="ChatdollKit AITuber Control API")
app.include_router(get_client_router(client))
app.include_router(get_comment_router(comment_monitor_manager))
