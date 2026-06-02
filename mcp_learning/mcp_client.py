import os, sys
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
print(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import llm
from langchain_core.prompts import PromptTemplate

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

    agent = create_agent(
        model = llm.ollama_llm,
        tools = tools,
        # system_prompt = "你是一个具有高德导航工具箱的导航智能体",
    )

    prompt_temp = PromptTemplate.from_template("你是一个导航智能助手，可以调用高德的mcp工具\n\n问题: {input}")
    prompt = prompt_temp.format(input = "帮我规划一条从成都清园小区到古蔺白沙小学的路线")

    resp = await agent.ainvoke(prompt)

    print(resp)


if __name__ == "__main__":
    asyncio.run(create_and_run_mapAgent())