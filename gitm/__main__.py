import typer


app = typer.Typer()


@app.command()
def hello() -> None:
    """
    This command will Create Tables in your postgresql instance \n
    -> Create Site table \n
    -> Create Metric table
    """
    print("Heloo")

def run() -> None:
    app()

if __name__ == "__main__":
    run()
