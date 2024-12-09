import json
import os
from abc import abstractmethod

from dashscope.api_entities.dashscope_response import Message

from prompt import user_prompt


class ModelProvider:
    """模型接入基类"""

    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.max_retry_times = 3

    def __call__(self, prompt, chat_history, *args):
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_times:
            cur_retry_time += 1
            try:
                messages = [Message(role="system", content=prompt)]
                for his in chat_history:
                    messages.append(Message(role="user", content=his[0]))
                    messages.append(Message(role="system", content=his[1]))
                messages.append(Message(role="user", content=user_prompt))
                return json.loads(self.chat(messages, *args))
            except Exception as err:
                print("调用大模型出错: {}".format(err))

    @abstractmethod
    def chat(self, *args, **kwargs):
        pass
