from typer import Typer

from .solutions import day01, day02, day03, day04

app = Typer()
app.command("day01")(day01.main)
app.command("day02")(day02.main)
app.command("day03")(day03.main)
app.command("day04")(day04.main)
