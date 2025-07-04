import typer
from rich import print
import cards
import os
from pathlib import Path
from contextlib import contextmanager
from typing import List, Optional
from rich.table import Table
from rich.box import SIMPLE

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Cards is a small command line task tracking application.
    """
    if ctx.invoked_subcommand is None:
        list_cards(owner=None, state=None)


@app.command()
def add(summary: List[str], owner: str = typer.Option(None, "-o", "--owner")):
    """
    Add a card to the db.
    """
    joined = " ".join(summary) if summary else None
    with cards_db() as db:
        db.add_card(cards.Card(joined, owner, state="todo"))


@app.command()
def config():
    """
    List the path to the Cards db.
    """
    with cards_db() as db:
        print(db.path())


@app.command()
def count():
    """
    Return the number of cards in db.
    """
    with cards_db() as db:
        print(db.count())


@app.command()
def delete(card_id: int):
    """
    Remove card in db with given id.
    """
    with cards_db() as db:
        try:
            db.delete_card(card_id)
        except cards.InvalidCardId:
            print(f"Error: invalid card id {card_id}")


@app.command()
def finish(card_id: int):
    """
    Set a card state to 'done'.
    """
    with cards_db() as db:
        try:
            db.finish(card_id)
        except cards.InvalidCardId:
            print(f"Error: invalid card id {card_id}")


@app.command("list")
def list_cards(
    owner: Optional[str] = typer.Option(None, "-o", "--owner"),
    state: Optional[str] = typer.Option(None, "-s", "--state"),
):
    """
    List cards in the db.
    """
    with cards_db() as db:
        the_cards = db.list_cards(owner=owner, state=state)
        table = Table(box=SIMPLE)
        table.add_column("ID")
        table.add_column("state")
        table.add_column("owner")
        table.add_column("summary")
        for t in the_cards:
            owner = "" if t.owner is None else t.owner
            table.add_row(str(t.id), t.state, owner, t.summary)
        print(table)


@app.command()
def start(card_id: int):
    """
    Set a card state to 'in prog'.
    """
    with cards_db() as db:
        try:
            db.start(card_id)
        except cards.InvalidCardId:
            print(f"Error: invalid card id {card_id}")


@app.command()
def update(
    card_id: int,
    owner: str = typer.Option(None, "-o", "--owner"),
    summary: List[str] = typer.Option(None, "-s", "--summary"),
):
    """
    Modify a card in db with given id with new info.
    """
    joined = " ".join(summary) if summary else None
    with cards_db() as db:
        try:
            db.update_card(card_id, cards.Card(joined, owner, state=None))
        except cards.InvalidCardId:
            print(f"Error: invalid card id {card_id}")


@app.command()
def version() -> None:
    """
    Return version of cards application.
    """
    print(cards.__version__)


def get_path() -> Path:
    db_path_env = os.getenv("CARDS_DB_DIR", "")
    if db_path_env:
        db_path = Path(db_path_env)
    else:
        db_path = Path.home() / "cards_db"
    return db_path


@contextmanager
def cards_db():
    db_path = get_path()
    db = cards.CardsDB(db_path)
    yield db
    db.close()


if __name__ == "__main__":
    app()
