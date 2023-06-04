import typer
from pattern import get_msg, patterns
import subprocess


app = typer.Typer()


@app.command()
def commit(msg:str) -> None:
    """
    This command will Create Tables in your postgresql instance \n
    -> Create Site table \n
    -> Create Metric table
    """
    # subprocess.run(["git", "status"]) 
    msg_commit = get_msg(msg)
    print(f"git commit -m \"{msg_commit}\"")
    subprocess.run(["git", "commit", "-m", msg_commit]) 

@app.command()
def acommit(msg:str) -> None:
    """
    This command will Create Tables in your postgresql instance \n
    -> Create Site table \n
    -> Create Metric table
    """
    # subprocess.run(["git", "status"]) 
    msg_commit = get_msg(msg)
    print("git add .")
    subprocess.run(["git", "add", "."]) 
    print(f"git commit -m \"{msg_commit}\"")
    subprocess.run(["git", "commit", "-m", msg_commit]) 

@app.command()
def get_pattern() -> None:
    for index, pattern in enumerate(patterns):
        print(index, pattern)
 
def run() -> None:
    app()
    # print(sys.argv[1:])

if __name__ == "__main__":
    run()

# @app.command()
# def add_pattern(regex:str, emoji:str, description) -> None:
#     patterns.append(Pattern(regex=regex, emoji=emoji, description=description))
#     print(patterns)

# @app.command()
# def update_pattern(index:int, pattern:str, emoji:str) -> None:
#     ...

# @app.command()
# def remove_pattern(index:int) -> None:
#     ...

# @app.command()
# def test() -> None:
#     migrate()