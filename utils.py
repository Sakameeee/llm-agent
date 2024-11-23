import json
import os.path

from langchain_community.tools.tavily_search import TavilySearchResults


def _get_workdir_root():
    workdir_root = os.environ.get("WORKDIR_ROOT", "./data/llm_result")
    return workdir_root


WORKDIR_ROOT = _get_workdir_root()


def read_file(file_name):
    if not os.path.exists(file_name):
        return f"{file_name} not exits, please check file before read"

    with open(file_name, "r") as f:
        return "\n".join(f.readlines())


def append_to_file(file_name, content):
    file_name = os.path.join(WORKDIR_ROOT, file_name)
    if not os.path.exists(file_name):
        return f"{file_name} not exits, please check file before read"

    with open(file_name, 'a') as f:
        f.write(content)

    return "append content to file success"


def write_to_file(file_name, content):
    file_name = os.path.join(WORKDIR_ROOT, file_name)
    if not os.path.exists(WORKDIR_ROOT):
        os.makedirs(WORKDIR_ROOT)

    with open(file_name, 'w') as f:
        f.write(content)

    return "append content to file success"


def search_from_net(query):
    tavily = TavilySearchResults(max_result=5)

    try:
        """
        ret:
        [{
            "content": "",
            "url": "",
        }]
        """
        ret = tavily.invoke(input=query)
        content_list = [obj["content"] for obj in ret]
        return "\n".join(content_list)
    except Exception as err:
        return "search err: {}".format(err)


utils_info = [
    {
        "name": "read_file",
        "description": "read file from agent generate, should write file before read",
        "args": [{
            "name": "file_name",
            "type": "string",
            "description": "read file name"
        }]
    },
    {
        "name": "append_to_file",
        "description": "append llm content to file",
        "args": [{
            "name": "file_name",
            "type": "string",
            "description": "write file name"
        }, {
            "name": "content",
            "type": "string",
            "description": "content to append"
        }]
    },
    {
        "name": "write_to_file",
        "description": "write llm content to file",
        "args": [{
            "name": "file_name",
            "type": "string",
            "description": "write file name"
        }, {
            "name": "content",
            "type": "string",
            "description": "content to write"
        }]
    },
    {
        "name": "search_from_net",
        "description": "this is a search engine, you can gain additional knowledge thought this search engine"
                       "when you are unsure of what large model return",
        "args": [{
            "name": "query",
            "type": "string",
            "description": "search query to look up"
        }]
    },
]

util_map = {
    "read_file": read_file,
    "append_to_file": append_to_file,
    "write_to_file": write_to_file,
    "search_from_net": search_from_net
}


def gen_utils_desc():
    """根据工具信息生成工具的 prompt"""
    utils_desc = []
    for idx, t in enumerate(utils_info):
        args_desc = []
        for info in t["args"]:
            args_desc.append({
                "name": info["name"],
                "description": info["description"],
                "type": info["type"]
            })
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        util_desc = f"{idx + 1}, {t['name']}, args: {args_desc}"
        utils_desc.append(util_desc)

    utils_prompt = "\n".join(utils_desc)
    return utils_prompt
