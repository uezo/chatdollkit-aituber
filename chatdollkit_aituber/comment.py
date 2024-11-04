import multiprocessing
from typing import Callable, Optional
import pytchat


class CommentMonitor:
    def __init__(self, process_comment: Callable):
        self.process_comment = process_comment

    def start_monitoring(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive():
            for c in chat.get().sync_items():
                self.process_comment(c)


class CommentMonitorManager:
    def __init__(self, process_comment: Callable):
        self.comment_monitor = CommentMonitor(process_comment)
        self.process: Optional[multiprocessing.Process] = None
        self.video_id: Optional[str] = None

    def run_monitor(self, video_id: str):
        self.comment_monitor.start_monitoring(video_id)

    def start(self, video_id: str) -> bool:
        if self.process and self.process.is_alive():
            return False

        self.process = multiprocessing.Process(
            target=self.run_monitor,
            args=(video_id,)
        )
        self.process.start()
        self.video_id = video_id
        return True

    def stop(self) -> bool:
        if not self.process or not self.process.is_alive():
            return False

        self.process.terminate()
        self.process.join()
        self.video_id = None
        return True

    def get_status(self):
        is_running = bool(self.process and self.process.is_alive())
        return is_running, self.video_id if is_running else None
