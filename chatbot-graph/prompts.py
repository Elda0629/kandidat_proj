# prompts.py

def build_triage_prompt(field_name, options, user_message):
    """Generates the prompt for asking/parsing a single triage field."""
    
    option_list = "\n- ".join(options)
    
    # Handling for boolean (which has no options list)
    if field_name == "contacts_critical_systems":
        prompt_options = "This is a simple yes/no question."
    else:
        prompt_options = f"""
These are the only allowed options:
- {option_list}
"""

    return f"""
    You are collecting information about a medical device. 
    The specific piece of information you need right now is **{field_name}**.

    First, analyze the user's last message to see if you can extract the answer.
    User's message: "{user_message}"

    {prompt_options}

    - If you can confidently determine the correct option from the user's message, 
      call the tool `set_field` with `field="{field_name}"` and the correct `value`.
    
    - If you cannot determine the value, or the user did not provide it,
      ask the user a clear, simple question to get this information. 
      If they seem confused, briefly explain the concept.
    """