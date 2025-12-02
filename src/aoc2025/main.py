from typer import Typer

from .solutions import day01

app = Typer()
app.command("day01")(day01.main)
