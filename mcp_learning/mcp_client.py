import os, sys
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
print(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import llm

async def create_mcp_client():
    mcp_key = os.environ.get("AMAP_KEY")

    mcp_config = {
        "amap" : {
            "url" : f"http://mcp.amap.com/sse?key={mcp_key}",
            "transport" : "sse"
        }
    }

    client = MultiServerMCPClient(mcp_config)

    tools = await client.get_tools()
    
    return client, tools

async def create_and_run_mapAgent():
    client, tools = await create_mcp_client()
    # llm = ChatOllama(
    #     model = "qwen3.5:0.8b",
    #     # tools = tools,
    #     # system_prompt = "你是一个具有高德导航工具箱的导航智能体"
    # )

    agent = create_agent(
        model = llm.bailian_llm,
        tools = tools,
        system_prompt = "你是一个具有高德导航工具箱的导航智能体",
    )

    while True:
        user_input = input("🔹 你想让 Agent 做什么？\n> ")
        resp = await agent.ainvoke(
            {"messages" : [{"role" : "user", "content" : user_input}]}
        )

        print(resp)

        # for key, values in resp.items():
        #     print("key:\n{}".format(key))
        #     print("values:")
        #     for value in values:
        #         print(value)
        #     print()

        # print("-------------------------------------")
        # print(resp["messages"][-1].content)
        
        # continue_ques = input("是否继续对话(y or n)?:\n")
        # while continue_ques not in ["y", "n"]:
        #     continue_ques = input("你猪脑子吗?看不懂人话?滚回去重新输一遍，再错把你骨灰扬了！！！\n")
        #     if continue_ques not in ["y", "n"]:
        #         print("说不明白了！算了，我妈不让我跟傻子玩儿")
        #         break_conversation = True
        #         break
        # if continue_ques == "n" or break_conversation:
        #     break


if __name__ == "__main__":
    asyncio.run(create_and_run_mapAgent())