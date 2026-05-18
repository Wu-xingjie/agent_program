#coding=utf-8
import tool
import prompt
from langchain_ollama import ChatOllama
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain.agents import create_agent

my_llm = ChatOllama(
    model = "qwen3.5:0.8b",
    temperature = 0.5
)

my_agent = create_agent(
    model = my_llm,
    tools = tool.tools,
    system_prompt = prompt.SYSTEM_PROMPT
    )

if __name__ == "__main__":
    break_conversation = False
    while True:
        user_input = input("🔹 你想让 Agent 做什么？\n> ")
        resp = my_agent.invoke(
            {"messages" : [{"role" : "user", "content" : user_input}]}
        )
        
        for key, values in resp.items():
            print("key:\n{}".format(key))
            print("values:")
            for value in values:
                print(value)
            print()

        print("-------------------------------------")
        print(resp["messages"][-1].content)
        
        continue_ques = input("是否继续对话(y or n)?:\n")
        while continue_ques not in ["y", "n"]:
            continue_ques = input("你猪脑子吗?看不懂人话?滚回去重新输一遍，再错把你骨灰扬了！！！\n")
            if continue_ques not in ["y", "n"]:
                print("说不明白了！算了，我妈不让我跟傻子玩儿")
                break_conversation = True
                break
        if continue_ques == "n" or break_conversation:
            break