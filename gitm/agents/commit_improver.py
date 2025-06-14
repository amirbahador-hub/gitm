# agents/commit_improver.py
from langchain_core.language_models import BaseChatModel
from gitm.utils.prompt_builder import build_commit_prompt

def improve_commit(commit_msg: str, llm: BaseChatModel) -> str:
    prompt = build_commit_prompt(commit_msg)
    response = llm.invoke(prompt)
    return response.content.strip()
