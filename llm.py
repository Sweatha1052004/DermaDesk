import litellm

def get_completion(messages, tools):
    """
    Standard completion function for DermaDesk.
    Note: Removed the trailing space from the model name.
    """
    return litellm.completion(
        # CRITICAL: No extra spaces at the end of the name
        model="ollama/gemini-3-flash-preview:cloud", 
        messages=messages,
        tools=tools,
        tool_choice="auto",
        api_base="http://localhost:11434",
        temperature=0.0,
        # In your llm.py completion call:
        stop=["### User:", "### Assistant:", "User:", "Bot:"]
        # Adding num_ctx ensures the model has enough memory for conversation history
        #num_ctx=4096 
    )