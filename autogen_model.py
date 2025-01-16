from autogen_ext.models.openai import OpenAIChatCompletionClient

class AutogenModel:
    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input parameters for configuring the OpenAI model.
        """
        return {
            "required": {
                "model_name": ([
                    "gpt-4o",
                    "gpt-4o-mini",
                    "chatgpt-4o-latest",
                    "gpt-3.5-turbo",
                    "deepseek-chat",
                    "deepseek-coder",
                ], {"default": "gpt-4o-mini"}),
                "base_url": ("STRING", {"multiline": False, "default": "https://api.openai.com/v1"}),
                "api_key": ("STRING", {"multiline": False, "default": "openai_api_key"}),
                "vision": (["True", "False"], {"default": "False"}),
                "function_calling": (["True", "False"], {"default": "False"}),
                "json_output": (["True", "False"], {"default": "False"}),
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("autogen_model",)
    FUNCTION = "initialize_model"
    CATEGORY = "Autogen"

    def initialize_model(self, model_name, base_url, api_key, vision, function_calling, json_output):
        """
        Initialize the OpenAI model with the provided configuration.
        """
        try:
            # Initialize the OpenAI client
            autogen_model = OpenAIChatCompletionClient(
                model=model_name,
                base_url=base_url,
                api_key=api_key,
                model_capabilities={
                    "vision": vision == "True",
                    "function_calling": function_calling == "True",
                    "json_output": json_output == "True",
                },
            )
            print(f"[AutogenModel] Successfully initialized model: {model_name}")
            return (autogen_model,)
        except Exception as e:
            print(f"[AutogenModel] Failed to initialize model: {e}")
            return (None,)
