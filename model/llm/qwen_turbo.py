import os

import dashscope
from dotenv import load_dotenv

from model.llm.model_provider import ModelProvider

load_dotenv()


class QwenTurbo(ModelProvider):
    """通义千问 turbo 大模型"""

    def __init__(self):
        super().__init__()

    def chat(self, messages, *args):
        response = dashscope.Generation.call(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=os.getenv('API_KEY'),
            model=os.getenv('MODEL_NAME'),  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages,
            result_format='message'
        )

        if response.status_code != 200:
            raise Exception(response.message)

        return response.output.choices[0].message.content
