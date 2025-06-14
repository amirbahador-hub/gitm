import subprocess
import sys

import typer

from gitm.agents.commit_improver import improve_commit
from gitm.llm_plugin_loader import get_llm

app = typer.Typer()


@app.command()
def commit(msg: str) -> None:
    """
    This command will improve the commit message using the LLM
    """
    msg_commit = improve_commit(msg, get_llm())
    input(f"\n👉 About to run:\n\n    git commit -m \"{msg_commit}\"\n\nPress Enter to continue, or Ctrl+C to cancel... ")
    subprocess.run(["git", "commit", "-m", msg_commit])




@app.command()
def acommit(msg: str) -> None:
    """
    This command will improve the commit message using the LLM
    """
    # subprocess.run(["git", "status"])
    msg_commit = improve_commit(msg, get_llm())
    print("git add .")
    subprocess.run(["git", "add", "."])
    print(f'git commit -m "{msg_commit}"')
    subprocess.run(["git", "commit", "-m", msg_commit])


def run() -> None:
    app()


if __name__ == "__main__":
    run()
