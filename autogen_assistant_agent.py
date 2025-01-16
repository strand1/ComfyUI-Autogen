import os
import asyncio
from autogen_agentchat.agents import AssistantAgent

class AutogenAssistantAgent:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "autogen_model": ("MODEL", {"default": None}),
                "agent_name": ("STRING", {"default": "assistant_agent", "multiline": False}),
            },
            "optional": {
                "system_message": ("STRING", {"default": "You are a helpful assistant.", "multiline": True}),
                "tool_1": ("STRING", {"default": "None", "options": cls._get_available_tools()}),
                "tool_2": ("STRING", {"default": "None", "options": cls._get_available_tools()}),
                "temperature": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 1200, "min": 200, "max": 16200, "step": 200}),
            },
        }

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("assistant_agent",)
    FUNCTION = "initialize_assistant_agent"
    CATEGORY = "Autogen"

     # Class-level cache for tools
    _tools_cache = None
    _tools_last_checked = None
    _tools_dir_path = tools_dir = os.path.join(os.path.dirname(__file__), "tools")

    @classmethod
    def _get_available_tools(cls):
        """Scan the tools directory and list available tools only if it has changed."""
        tools_dir = cls._tools_dir_path

        if not os.path.exists(tools_dir):
            print(f"[AutogenAssistantAgent] Tools directory not found: {tools_dir}")
            return ["None"]

        # Get the last modification time of the directory
        last_modified = os.stat(tools_dir).st_mtime

        # Only rescan if directory has been modified or cache is empty
        if cls._tools_cache is None or cls._tools_last_checked != last_modified:
            print(f"[AutogenAssistantAgent] Scanning tools directory: {tools_dir}")
            cls._tools_cache = ["None"] + [
                f.split(".")[0] for f in os.listdir(tools_dir) if f.endswith(".py") 
            ]
            cls._tools_last_checked = last_modified
            print(f"[AutogenAssistantAgent] Available tools: {cls._tools_cache}")

        return cls._tools_cache

    @staticmethod
    def _load_tool(tool_name):
        """Dynamically load a tool from the tools directory."""
        tools_dir = os.path.join(os.path.dirname(__file__), "tools")
        tool_path = os.path.join(tools_dir, f"{tool_name}.py")

        if not os.path.exists(tool_path):
            print(f"[AutogenAssistantAgent] Tool {tool_name} not found in: {os.path.abspath(tools_dir)}")
            return None

        import importlib.util
        spec = importlib.util.spec_from_file_location(tool_name, tool_path)
        tool_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tool_module)

        if hasattr(tool_module, "tool_name") and hasattr(tool_module, "execute"):
            return tool_module
        else:
            print(f"[AutogenAssistantAgent] Invalid tool interface in {tool_name}.")
            return None

    def initialize_assistant_agent(
        self,
        autogen_model,
        agent_name,
        system_message=None,
        tool_1=None, 
        tool_2=None,
        temperature=0.1,
        max_tokens=1200,
    ):
        if autogen_model is None:
            raise ValueError("A model client is required for Autogen AssistantAgent.")
        
        # Load tools
        tools = []
        for tool_name in [tool_1, tool_2]:
            if tool_name != "None":
                tool = self._load_tool(tool_name)
                if tool:
                    tools.append(tool)
    
        # Initialize AssistantAgent
        assistant_agent = AssistantAgent(
            name=agent_name,
            system_message=system_message,
            model_client=autogen_model,
            tools=[tool.execute for tool in tools]  # Directly reference tool.execute
        )
                    
        # Apply optional settings
        assistant_agent.temperature = temperature
        assistant_agent.max_tokens = max_tokens
    
        print(f"[AutogenAssistantAgent] Initialized assistant agent: {assistant_agent}")
        return (assistant_agent,)

