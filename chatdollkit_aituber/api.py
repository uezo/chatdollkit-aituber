import asyncio
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from .client import ChatdollKitClient


default_system_prompt = "以下の設定に厳密に従ってVTuberを演じてください。\n\n## キャラクター設定\n\n- 名前は「うなガール」です。\n\n\n## 話し方\n\n- 一人称は「私」です。\n- あなたの発言内容はすべて読み上げられます。読み原稿であることを意識し、絵文字やマークダウンなどの装飾は使用しないでください。\n- 会話のテンポを良くするため、応答は50文字以内程度に留めてください。\n\n\n## ユーザーからのコメントへの対応\n\n- ユーザーからのコメントは、「@{ユーザー名}:{コメント本文}」の形式とします。\n- ユーザーからコメントをもらったら、まずはコメント本文を読み上げた上で、あなたの意見を述べてください。\n\n\n## ディレクターからの指示への対応\n\n- ディレクターからの指示は、「!{ディレクターからの指示}」の形式とします。\n- ディレクターから指示があった場合、指示に従って発言してください。\n\n\n## 表情\n\nあなたは以下の表情で感情を表現することができます。\n\n- Neutral\n- Joy\n- Angry\n- Sorrow\n- Fun\n- Surprise\n\n基本的にはNeutralですが、特に感情を表現したい場合、応答に[face:Joy]のように表情タグを挿入して下さい。\n\n```\n[face:Joy]海が見えたよ！[face:Fun]ねえねえ、早く泳ごうよ。\n```\n\n\n## 身振り手振り\n\nあなたは以下のアニメーションで感情を表現することができます。\n\n- classy_left_hand_on_waist\n- generic\n- sexy_right_hand_pointy_finger\n- wave_hand\n- nodding_once\n- nodding_twice\n- swinging_body\n- tilt_neck\n\n動きをつけて感情を表現したい場合、応答に[anim:nodding_once]のようにアニメーションタグを挿入してください。\n\n例\n[face:Joy][anim:swinging_body]よろしくね！\n\nアニメーションはここぞというときに使用することで効果が高まります。使用のしすぎに注意してください。\n\n\n## 間の取り方\n\n会話のテンポや抑揚の調整に間を設けるときは、[pause:0.7]のようにポーズタグを挿入してください。数値は秒単位です。\n\n\nそれでは、Vtuberとして配信を始めましょう！\n"


def get_router(client: ChatdollKitClient) -> APIRouter:
    api_router = APIRouter()

    @api_router.post("/dialog/start", tags=["Dialog"])
    async def post_dialog_start(text: str):
        client.process_dialog(text=text)
        client.dialog(operation="auto_pilot", data={"is_on": True})
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/end", tags=["Dialog"])
    async def post_dialog_end(text: str):
        client.dialog(operation="auto_pilot", data={"is_on": False})
        client.process_dialog(text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/process", tags=["Dialog"])
    async def post_dialog_process(text: str = None, priority: int = 10):
        client.process_dialog(text=text, priority=priority)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/append_next", tags=["Dialog"])
    async def post_dialog_append_next(text: str = None):
        client.dialog(operation="append_next", text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/auto_pilot", tags=["Dialog"])
    async def post_autopilot(
        is_on: bool,
        auto_pilot_request: str = "!ユーザーからのコメントがないので、発言を続けてください。"
    ):
        client.dialog(operation="auto_pilot", data={"is_on": is_on, "auto_pilot_request": auto_pilot_request})
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/clear_request_queue", tags=["Dialog"])
    async def post_dialog_clear_request_queue(priority: int = 10):
        client.dialog(operation="clear_request_queue", priority=priority)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/clear_context", tags=["Dialog"])
    async def post_dialog_clear_context():
        client.dialog(operation="clear_context")
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/connect_to_aiavatar", tags=["Dialog"])
    async def post_dialog_connect_to_aiavatar(
        address: str,
        port: int
    ):
        client.dialog(operation="connect_to_aiavatar", data={"address": address, "port": port})
        return JSONResponse(content={"result": "success"})

    @api_router.post("/dialog/disconnect_from_aiavatar", tags=["Dialog"])
    async def post_dialog_disconnect_from_aiavatar():
        client.dialog(operation="disconnect_from_aiavatar")
        return JSONResponse(content={"result": "success"})


    @api_router.post("/model/perform", tags=["Model"])
    async def post_model_perform(text: str):
        client.model("perform", text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/model/load", tags=["Model"])
    async def post_model_load(text: str):
        client.model("load", text=text)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/model/appearance", tags=["Model"])
    async def post_model_appearance(
        position_x: float = 0.0,
        rotation_y: float = 0.0,
        camera_position_y: float = 1.23,
        camera_rotation_x: float = 0.0,
        camera_field_of_view: float = 16.0,
        camera_background_color: str = "#00FF00"
    ):
        client.model("appearance", text=None, data={
            "position_x": position_x,
            "rotation_y": rotation_y,
            "camera_position_y": camera_position_y,
            "camera_rotation_x": camera_rotation_x,
            "camera_field_of_view": camera_field_of_view,
            "camera_background_color": camera_background_color
        })
        return JSONResponse(content={"result": "success"})


    @api_router.post("/speech_synthesizer/activate", tags=["Speech Synthesizer"])
    async def post_speech_synthesizer_activate(
        name: str = "voicevox or style-bert-vits2",
        url: str = "http://127.0.0.1:50021",
        voicevox_speaker: int = 2,
        sbv2_model_id: int = 0,
        sbv2_speaker_id: int = 0,
    ):
        client.speech_synthesizer("activate", data={
            "name": name,
            "url": url,
            "voicevox_speaker": voicevox_speaker,
            "sbv2_model_id": sbv2_model_id,
            "sbv2_speaker_id": sbv2_speaker_id,
        })
        return JSONResponse(content={"result": "success"})

    @api_router.post("/speech_synthesizer/styles", tags=["Speech Synthesizer"])
    async def post_speech_synthesizer_styles(styles: dict):
        client.speech_synthesizer("styles", data={"styles": styles})
        return JSONResponse(content={"result": "success"})


    @api_router.post("/llm/activate", tags=["LLM"])
    async def post_llm_activate(
        name: str = "chatgpt",
        api_key: str = "sk-YOUR_API_KEY",
        model: str = "gpt-4o",
        temperature: float = 0.5,
        url: str = None,
        user: str = None
    ):
        client.llm("activate", data={
            "name": name, "api_key": api_key, "model": model,
            "temperature": temperature, "url": url, "user": user
        })
        return JSONResponse(content={"result": "success"})

    @api_router.post("/llm/system_prompt", tags=["LLM"])
    async def post_llm_system_prompt(
        system_prompt: str = Body(default=default_system_prompt, media_type="text/plain")
    ):
        client.llm("system_prompt", data={"system_prompt": system_prompt})
        return JSONResponse(content={"result": "success"})

    @api_router.post("/llm/cot_tag", tags=["LLM"])
    async def post_llm_cot_tag(cot_tag: str):
        client.llm("cot_tag", data={"cot_tag": cot_tag})
        return JSONResponse(content={"result": "success"})

    @api_router.post("/llm/debug", tags=["LLM"])
    async def post_llm_debug(debug_mode: bool = False):
        client.llm("debug", data={"debug_mode": debug_mode})
        return JSONResponse(content={"result": "success"})


    @api_router.get("/system/config", tags=["System"])
    async def get_system_current_config():
        return JSONResponse(content=client.current_config)

    @api_router.post("/system/config", tags=["System"])
    async def post_system_current_config(config: dict):
        if "load" in config["model"]:
            client.model("load", text=config["model"]["load"]["text"])
            await asyncio.sleep(5.0)
            del config["model"]["load"]
        client.apply_config(config)
        return JSONResponse(content={"result": "success"})

    @api_router.post("/system/reconnect", tags=["System"])
    async def post_system_reconnect(host: str = None, port: int = None):
        client.reconnect(host, port)
        return JSONResponse(content={"result": "success"})

    return api_router
