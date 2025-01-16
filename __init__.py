from .autogen_model import AutogenModel
from .autogen_assistant_agent import AutogenAssistantAgent
from .autogen_groupchat import AutogenGroupChat
from .autogen_code_executor import AutogenCodeExecutor

NODE_CLASS_MAPPINGS = {
    "AutogenModel": AutogenModel,
    "AutogenAssistantAgent": AutogenAssistantAgent,
    "AutogenGroupChat": AutogenGroupChat,
    "AutogenCodeExecutor": AutogenCodeExecutor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutogenModel": "Autogen Model",
    "AutogenAssistantAgent": "Autogen Assistant Agent",
    "AutogenGroupChat": "Autogen Group Chat",
    "AutogenCodeExecutor": "Autogen Code Executor",
}

# Optional: Specify a web directory for static assets (if applicable)
WEB_DIRECTORY = "./web"

# Export all variables for ComfyUI to recognize
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
