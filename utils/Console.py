import os
import sys
from rich.console import Console as RichConsole
from pyfiglet import Figlet

sys.path.append(os.path.realpath("."))

class Console:
    def __init__(self):
        self.rich_console = RichConsole()

    def show_dev_info(self):
        # Очистка экрана
        os.system("cls" if os.name == "nt" else "clear")
        # Создаем ASCII-арт с помощью pyfiglet с шрифтом "slant"
        figlet = Figlet(font="slant", width=200)
        ascii_art = figlet.renderText("Nod3r")
        self.rich_console.print(f"[bold cyan]{ascii_art}[/bold cyan]")
        print()

    def build(self) -> None:
        self.show_dev_info()
