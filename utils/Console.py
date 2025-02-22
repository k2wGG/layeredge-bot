import os
import sys
from rich.console import Console as RichConsole
from pyfiglet import Figlet

sys.path.append(os.path.realpath("."))

class Console:

    def __init__(self):
        self.rich_console = RichConsole()

    def show_dev_info(self):
        os.system("cls" if os.name == "nt" else "clear")

        figlet = Figlet(font="puffy", width=200)
        ascii_art = figlet.renderText("by mbiphes")

        self.rich_console.print(f"{ascii_art}")
        print()

    def build(self) -> None:
        self.show_dev_info()
        self.display_info()
