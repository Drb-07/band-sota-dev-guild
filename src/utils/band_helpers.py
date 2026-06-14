import asyncio
import json
from typing import Dict, Any, List

class MockBandRoom:
    def __init__(self, room_id: str):
        self.id = room_id
        self.logs: List[Dict[str, str]] = []

    async def send_message(self, text: str, author: str):
        message_payload = {"author": author, "text": text}
        self.logs.append(message_payload)
        print(f"\n💬 [{author} inside {self.id}]:\n{text}\n{'-'*50}")
        await asyncio.sleep(1)

    async def get_memory_logs(self) -> List[Dict[str, str]]:
        return self.logs

class MockBandClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.handlers: Dict[str, Any] = {}

    async def connect_agent(self, agent_handle: str):
        return MockAgentInstance(agent_handle, self)

class MockAgentInstance:
    def __init__(self, handle: str, client: MockBandClient):
        self.handle = handle
        self.client = client

    def on_message(self, func):
        self.client.handlers[self.handle] = func
        return func

    async def trigger_mock_mention(self, room: MockBandRoom, text: str, author: str):
        handler = self.client.handlers.get(self.handle)
        if handler:
            await handler(room, type('Msg', (object,), {"text": text, "author": author})())
