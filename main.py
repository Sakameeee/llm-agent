import time

from prompt import gen_prompt
from utils import util_map


def parser_thoughts(response):
    """解析响应"""
    try:
        thoughts = response.get("thoughts")
        observation = thoughts.get("speak")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        prompt = f"plan: {plan}\nreasoning: {reasoning}\ncriticism: {criticism}\nobservation: {observation}"
        return prompt
    except Exception as err:
        print("parser thoughts err: {}".format(err))


def agent_execute(query, max_request_times=10):
    """agent 执行任务"""
    cur_request_times = 0
    chat_history = []
    agent_scratch = ""

    while cur_request_times < max_request_times:
        cur_request_times += 1

        # 1.创建 prompt
        prompt = gen_prompt()
        print("开始调用大模型", flush=True)
        # 2.调用大模型
        start_time = time.time()
        response = ""
        end_time = time.time()
        print("调用大模型结束，耗时: {}".format(end_time - start_time), flush=True)

        if not response or not isinstance(response, dict):
            print("调用大模型错误，即将重试......", response)

        """
        response:
        {
            "action": {
                "name": "action name",
                "args": {
                    "args name": "args value"
                }
            },
            "thoughts": {
                "text": "thought",
                "plan": "plan",
                "criticism": "criticism",
                "speak": "speak",
                "reasoning": ""
            }
        }
        """
        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")

        if action_name == "finish":
            final_answer = action_args.get("answer")
            print("final_answer: ", final_answer)
            break

        # 3.解析响应
        observation = response.get("thoughts").get("speak")
        try:
            func = util_map.get(action_name)
            observation = func(**action_args)

        except Exception as err:
            print("调用工具异常: ", err)

        agent_scratch = agent_scratch + "\n" + observation
        user_msg = ""
        assistant_msg = ""
        chat_history.append([user_msg, assistant_msg])


def main():
    max_request_time = 10

    while True:
        query = input("请输入您的目标:")
        if query == "exit":
            return
        agent_execute(query, max_request_time)


if __name__ == '__main__':
    main()
