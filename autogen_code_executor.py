from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
import os

class AutogenCodeExecutor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "agent_name": ("STRING", {"default": "code_executor", "multiline": False}),
            },
            "optional": {
                "working_directory": ("STRING", {"default": os.getcwd(), "multiline": False}),
                "timeout": ("INT", {"default": 10, "min": 1, "max": 60, "step": 1}),
            },
        }

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("code_executor_agent",)
    FUNCTION = "initialize_code_executor"
    CATEGORY = "Autogen"

    def initialize_code_executor(self, agent_name, working_directory=None, allow_network=False, timeout=10):
        # Initialize the LocalCommandLineCodeExecutor
        local_executor = LocalCommandLineCodeExecutor(
            work_dir=working_directory or os.getcwd(),
            timeout=timeout,
        )

        # Create the CodeExecutorAgent
        code_executor_agent = CodeExecutorAgent(
            name=agent_name,
            code_executor=local_executor,
        )

        print(f"[AutogenCodeExecutor] Initialized code executor agent: {code_executor_agent}")
        return (code_executor_agent,)
