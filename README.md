# ComfyUI-Autogen
A collection of nodes for using Autogen with ComfyUI 
[AutoGen](https://github.com/microsoft/AutoGen)
(assistant agents, group chats, code executor, etc.)

## Features

1. **Autogen Model**  
   - Initializes an OpenAI-like model via `autogen_ext.models`.  
   - Lets you configure model name, base URL, API key, and optional capabilities like vision, function calling, and JSON output.

2. **Autogen Assistant Agent**  
   - Wraps an `AssistantAgent` from `autogen_agentchat.agents`.  
   - Lets you specify tools (by scanning a `tools` folder), temperature, max tokens, etc.  
   - Great for orchestrating more conversational or tool-using LLM tasks within ComfyUI.

3. **Autogen Code Executor**  
   - A node wrapping the `CodeExecutorAgent` from `autogen_agentchat.agents` with a local command-line executor.  
   - Enables code execution tasks, specifying a working directory, timeouts, etc.

4. **Autogen Group Chat**  
   - Leverages `RoundRobinGroupChat` to let multiple agents interact in a conversation.  
   - Terminates the chat based on a max number of messages or a specific terminate string.

## Requirements

```text
autogen-core
autogen-ext
autogen-agentchat
requests

## Todo
- vision models needs integration
