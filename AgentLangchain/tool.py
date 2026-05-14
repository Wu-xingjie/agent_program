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
      执行一条允许的 PowerShell 命令。当前仅支持：
        `ls <路径>`  
        示例: runSafeCommand("ls C:\\Users")
        示例: runSafeCommand("ls D:\\test\\dir")
    '''
    parts = command.strip().split(maxsplit=1)
    cmd_name = parts[0].lower()
    
    path = parts[1].strip() if len(parts) > 1 else "."
    # 构造实际要执行的命令（使用 PowerShell）
    # full_cmd = allowed[cmd_name].format(path=path)
    try:
        result = subprocess.run(parts, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"执行出错: {str(e)}"
    

tools = [getCurTime, runSafeCommand]