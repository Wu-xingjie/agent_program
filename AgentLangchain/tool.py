#coding=utf-8

from langchain_core.tools import tool
import datetime
import subprocess

@tool
def getCurTime() -> str:
    '''
    用于获取当前时间, 格式: 年-月-日 小时 ：分钟 : 秒钟
    '''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def runSafeCommand(command: str) -> str:
    '''
      执行一条安全的 Windows 命令，仅支持以下形式：
    - ls <路径>     : 列出目录内容，例如 "ls D:\\test"

    注意：command 参数必须是上述格式的字符串，不能包含管道符、PowerShell 专有命令（如 Get-Date）。
    其他命令一律拒绝。
    '''
    parts = command.strip().split(maxsplit=1)

    try:
        result = subprocess.run(parts, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"执行出错: {str(e)}"
    

tools = [getCurTime, runSafeCommand]