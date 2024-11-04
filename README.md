# ChatdollKit AITuber Controller

A RESTful API server to control ChatdollKit-based AITuber 💬

## 🚀 Quick Start

- Setup [ChatdollKit AITuber Demo](https://github.com/uezo/ChatdollKit) and start the app.

- Install ChatdollKit AITuber Controller from this repository.

    ```sh
    pip install git+https://github.com/uezo/chatdollkit-aituber
    ```

- Make `run.py`.

    ```python
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
    ```

- Run controller.

    ```sh
    uvicorn run:app
    ```

    Open http://localhost:8000 to get started.

- Call `/dialog/start` with text to make AITuber start broadcasting. (e.g. "挨拶して配信を開始してください。")

- Call `/dialog/end` to end broadcasting.

- If you want AITuber to react to listener's comments, call `/comment/start`.

Enjoy! 👍
