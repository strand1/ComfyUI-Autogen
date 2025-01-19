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
                "tool_1": ("STRING", {"default": "None"}),
                "tool_2": ("STRING", {"default": "None"}),
                "temperature": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 1200, "min": 200, "max": 16200, "step": 200}),
            },
        }

    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ("assistant_agent",)
    FUNCTION = "initialize_assistant_agent"
    CATEGORY = "Autogen"

    @staticmethod
    def _load_tool(tool_name):
        """Load a tool from the tools directory."""
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
            if tool_name and tool_name != "None":
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
