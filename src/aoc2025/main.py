from typer import Typer

from .solutions import day01, day02

app = Typer()
app.command("day01")(day01.main)
app.command("day02")(day02.main)
