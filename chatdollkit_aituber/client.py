import json
import socket
import traceback


class ChatdollKitClient:
    def __init__(self, host: str = "localhost", port: int = 8888):
        self.host = host
        self.port = port

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def close(self):
        self.client_socket.close()

    def send_message(self, endpoint: str, operation: str, *, text: str = None, priority: int = 10, payloads: dict = None):
        try:
            self.connect()

            message_dict = {
                "Endpoint": endpoint,
                "Operation": operation,
                "Text": text,
                "Priority": priority,
            }
            if payloads:
                message_dict["Payloads"] = payloads
            message = json.dumps(message_dict)

            self.client_socket.sendall((message + "\n").encode("utf-8"))
            print(f"Message sent: {message}")

        except Exception as ex:
            print(f"Failed to send message: {ex}\n{traceback.format_exc()}")

        finally:
            self.close()

    def dialog(self, operation: str, text: str = None, priority: int = 10):
        self.send_message("dialog", operation, text=text, priority=priority)

    def process_dialog(self, text: str, priority: int = 10):
        self.dialog("process", text=text, priority=priority)

    def clear_dialog_queue(self, priority: int = 0):
        self.dialog("clear", priority=priority)

    def model(self, text: str):
        self.send_message("model", "perform", text=text)

    def config(self, data: dict):
        self.send_message("config", "apply", payloads=data)
