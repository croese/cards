import typer
from rich import print
import cards

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Cards is a small command line task tracking application.
    """
    if ctx.invoked_subcommand is None:
        list_cards()


@app.command()
def add() -> None:
    """
    Add a card to the db.
    """
    print("TODO: add a card")


@app.command()
def config() -> None:
    """
    List the path to the Cards db.
    """
    print("TODO: config stuff")


@app.command()
def count() -> None:
    """
    Return the number of cards in db.
    """
    print("TODO: count the cards")


@app.command()
def delete() -> None:
    """
    Remove card in db with given id.
    """
    print("TODO: delete a card")


@app.command()
def finish() -> None:
    """
    Set a card state to 'done'.
    """
    print("TODO: finish a card")


@app.command("list")
def list_cards() -> None:
    """
    List cards in the db.
    """
    print("TODO: list cards")


@app.command()
def start() -> None:
    """
    Set a card state to 'in prog'.
    """
    print("TODO: start a card")


@app.command()
def update() -> None:
    """
    Modify a card in db with given id with new info.
    """
    print("TODO: modify card")


@app.command()
def version() -> None:
    """
    Return version of cards application.
    """
    print(cards.__version__)
