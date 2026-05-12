import requests
import re
from prompt import SYSTEM_PROMPT
from tool import TOOL_MAP

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"

def callModal(prompt_text: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt_text,
        "stream": False,
        "options": {
            "temperature": 0.2,   # 确定性输出，便于格式解析
            "num_predict": 1024,
        }
    }
    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print("模型运行消息：")
    for key, val in data.items():
        print("{} -> {}".format(key, val))
    return data["response"]

def parse_latest_action(text: str):
    """
    从模型最近一次输出中，找到最后一个 Action: 行，提取工具名和参数。
    返回 (tool_name, arg) 或 None。
    """
    # 匹配 Action: 工具名[参数]
    pattern = r"Action:\s*([a-zA-Z_]+)\[(.*?)\]"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        # 取最后一个 Action
        return matches[-1][0].strip(), matches[-1][1].strip()
    return None

def has_final_answer(text: str):
    """检查是否包含 Final Answer:"""
    return "Final Answer:" in text

def execute_tool(tool_name: str, arg: str) -> str:
    func = TOOL_MAP.get(tool_name)
    if not func:
        return f"未知工具: {tool_name}"
    try:
        if arg == "":
            return func()
        else:
            # 工具函数一般只接收一个参数
            return func(arg)
    except Exception as e:
        return f"工具调用异常: {str(e)}"

# 利用列表存储对话历史，初步实现记忆功能
chat_history = [{"role" : "system", "massage" : SYSTEM_PROMPT}]

def runAgent(user_query : str, max_turn = 1):
    turn = 0
    chat_history.append({"role" : "user", "massage" : user_query})
    while turn < max_turn:
        turn +=1
        print("\n[INFO] 第{}次迭代".format(turn))
        # 思考：每次循环都将对话历史组装为提示词，并输入给大模型
        massage = ""
        for chat in chat_history:
            if chat["role"] == "system":
                massage += "System : {}\n".format(chat["massage"])
            elif chat["role"] == "user":
                massage += "User : {}\n".format(chat["massage"])
            else:
                massage += "Assistant : {}\n".format(chat["massage"])

        # 调用LLM
        resp = callModal(massage)
        print("[INFO] resp -> {}".format(resp))

        if has_final_answer(resp):
            final_answer = resp.split()[-1].strip()
            print("最终回复： \n{}".format(final_answer))
            return final_answer
        
        action = parse_latest_action(resp)
        if action != None:
            tool_name, arg = action
            print(f"🔧 调用工具: {tool_name}[{arg}]")
            observation = execute_tool(tool_name, arg)
            print(f"👀 观察结果: {observation}")
            observation_massage = "Observation : {}".format(observation)
            print("[INFO] observation: \n{}".format(observation_massage))
            chat_history.append(
                {"role" : "Assistance", "massage" : observation_massage}
            )
    print("[INFO] 迭代达到最大次数")


if __name__ == "__main__":
    continue_ask = True
    while continue_ask:
        user_input = input("🔹 你想让 Agent 做什么？\n> ")
        runAgent(user_input)
        continue_ques = input("是否继续对话(y or n)?:\n")
        while continue_ques not in ["y", "n"]:
            continue_ques = input("你猪脑子吗?看不懂人话?滚回去重新输一遍，再错把你骨灰扬了！！！\n")
        if continue_ques == "n":
            break
    # 帮我查询当前时间？帮我列举出D:\github_project\agent_program中的所有文件和文件夹