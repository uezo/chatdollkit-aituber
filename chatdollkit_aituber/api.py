from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .client import ChatdollKitClient


class ConfigRequest(BaseModel):
    system_prompt: str = None
    autopilot_request: str = None


def get_router(client: ChatdollKitClient) -> APIRouter:
    api_router = APIRouter()

    @api_router.post("/dialog/start", tags=["Dialog"])
    async def post_dialog_start(text: str):
        client.process_dialog(text=text)
        client.dialog(operation="auto_on")
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/end", tags=["Dialog"])
    async def post_dialog_end(text: str):
        client.dialog(operation="auto_off")
        client.process_dialog(text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/process", tags=["Dialog"])
    async def post_dialog_process(text: str = None, priority: int = 10):
        client.process_dialog(text=text, priority=priority)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/autopilot", tags=["Dialog"])
    async def post_autopilot(is_on: bool):
        if is_on:
            client.dialog(operation="auto_on")
        else:
            client.dialog(operation="auto_off")
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/{operation}", tags=["Dialog"])
    async def post_dialog(operation: str, text: str = None, priority: int = 10):
        client.dialog(operation=operation, text=text, priority=priority)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/model/perform", tags=["Model Performance"])
    async def post_model_perform(text: str):
        client.model(text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/config/update", tags=["Configuration"])
    async def post_config_update(config_request: ConfigRequest):
        client.config(config_request.model_dump(exclude_unset=True, exclude_none=True))
        return JSONResponse(content={"result": "success"})

    return api_router
