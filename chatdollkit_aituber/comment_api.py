from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .comment import CommentMonitorManager


def get_router(comment_monitor_manager: CommentMonitorManager) -> APIRouter:
    api_router = APIRouter()

    @api_router.post("/comment/start", tags=["YouTube Comment"])
    def post_comment_start(video_id: str):
        success = comment_monitor_manager.start(video_id)
        return JSONResponse(content={"status": "started" if success else "already_running"})

    @api_router.post("/comment/stop", tags=["YouTube Comment"])
    def post_comment_stop():
        success = comment_monitor_manager.stop()
        return JSONResponse(content={"status": "stopped" if success else "error"})

    @api_router.get("/comment/status", tags=["YouTube Comment"])
    def get_status():
        is_running, video_id = comment_monitor_manager.get_status()
        return JSONResponse(content={"running": is_running, "video_id": video_id})

    return api_router
