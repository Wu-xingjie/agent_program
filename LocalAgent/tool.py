import os
import datetime
import subprocess

# 定义时间获取工具
def getCurTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 定义文件运行命令函数
def runSafeCommand(command: str):
    # 预定义白名单命令映射到 PowerShell 或正斜杠转换
    allowed = {
        "ls": "powershell -Command \"Get-ChildItem -Path '{path}'\""
    }
    parts = command.strip().split(maxsplit=1)
    cmd_name = parts[0].lower()
    if cmd_name not in allowed:
        return f"❌ 命令 '{cmd_name}' 不在白名单中。"
    
    path = parts[1].strip() if len(parts) > 1 else "."
    # 构造实际要执行的命令（使用 PowerShell）
    full_cmd = allowed[cmd_name].format(path=path)
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"执行出错: {str(e)}"


# 工具映射表
TOOL_MAP = {
    "getCurTime": getCurTime,
    "runSafeCommand": runSafeCommand,
}