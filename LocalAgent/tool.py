import os
import datetime
import subprocess

# 定义时间获取工具
def getCurTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 定义文件运行命令函数
def runSafeCommand(command : str):
    try:
        safe_commands = ["ls"]
        input_commands = command.strip().split()[0] 
        command_name = input_commands.lower()
        if command_name in safe_commands:
            raise RuntimeError("[ERROR] 命令{}不在白名单中，无法正常运行!".format(command_name))
        run_command = subprocess.run(input_commands, capture_output = True, text = True, timeout = 10)
        if run_command.returncode == 0:
            return run_command.stdout
        else:
            return run_command.stderr
    except Exception as e:
        print(e)


# 工具映射表
TOOL_MAP = {
    "getCurTime": getCurTime,
    "runSafeCommand": runSafeCommand,
}