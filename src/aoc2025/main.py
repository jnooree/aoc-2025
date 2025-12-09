from typer import Typer

from .solutions import (
    day01,
    day02,
    day03,
    day04,
    day05,
    day06,
    day07,
    day08,
    day09,
)

app = Typer()
app.command("day01")(day01.main)
app.command("day02")(day02.main)
app.command("day03")(day03.main)
app.command("day04")(day04.main)
app.command("day05")(day05.main)
app.command("day06")(day06.main)
app.command("day07")(day07.main)
app.command("day08")(day08.main)
app.command("day09")(day09.main)
