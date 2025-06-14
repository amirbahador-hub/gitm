def build_commit_prompt(message: str) -> str:
    """
    Generate a prompt to improve a commit message using Gitmojis.
    """
    return f"""Improve the following git commit message by making it more descriptive
and adding a relevant Gitmoji.

Original: {message}

Improved:"""


def build_generic_prompt(task_description: str, input_text: str) -> str:
    """
    Build a general-purpose prompt given a task and input.
    Useful for debugging or rapid iteration.
    """
    return f"""{task_description}

Input:
{input_text}

Output:"""
