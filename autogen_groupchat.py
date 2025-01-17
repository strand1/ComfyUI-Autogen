from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
import asyncio
import sys
import io

class AutogenGroupChat:
    def __init__(self):
        self.chat_log = []  # Store interactive chat log
        self.last_message = None  # Store the last message

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "agent_1": ("AGENT", {"default": None}),
                "agent_2": ("AGENT", {"default": None}),
                "task_input": ("STRING", {"default": "Provide a task description here.", "multiline": True}),
            },
            "optional": {
                "agent_3": ("AGENT", {"default": None}),
                "agent_4": ("AGENT", {"default": None}),
                "max_messages": ("INT", {"default": 10, "min": 1, "max": 100, "step": 1}),
                "terminate_string": ("STRING", {"default": "TERMINATE", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("console_output", "last_chat")
    FUNCTION = "run_group_chat"
    CATEGORY = "Autogen"

    def run_group_chat(self, agent_1, agent_2, task_input, agent_3=None, agent_4=None, 
                          max_messages=10, terminate_string="TERMINATE"):
        # Redirect console output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Initialize participants
            participants = [agent_1, agent_2]
            if agent_3:
                participants.append(agent_3)
            if agent_4:
                participants.append(agent_4)

            # Create termination conditions
            max_msg_termination = MaxMessageTermination(max_messages=max_messages)
            text_termination = TextMentionTermination(terminate_string)
            combined_termination = max_msg_termination | text_termination

            # Initialize PlannerGroupChat
            team = RoundRobinGroupChat(participants=participants, termination_condition=combined_termination)

            print(f"[AutogenGroupChat] Initialized with {len(participants)} participants.")

            chat_output = []

            async def capture_chat():
                async for task_result in team.run_stream(task=task_input):
                    if hasattr(task_result, "messages"):
                        for message in task_result.messages:
                            self.chat_log.append(f"{message.source}: {message.content}")
                            self.last_message = f"{message.source}: {message.content}"
                            print(f"[Interactive Chat] {self.last_message}")
                            chat_output.append(f"{message.source}: {message.content}")
            
                            # Clean and process the last message
                            if message.content.strip().endswith(terminate_string):
                                self.last_message = message.content.strip()[:-len(terminate_string)].strip()
                            else:
                                self.last_message = message.content.strip()

            asyncio.run(capture_chat())

        except RuntimeError as e:
            print(f"[AutogenGroupChat] Runtime error: {e}")
            return "Error during execution", self.last_message, sys.stdout.getvalue()

        # Capture console output and reset stdout
        console_output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return console_output, self.last_message
