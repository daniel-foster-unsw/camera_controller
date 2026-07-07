"""
main.py

Program entry point.
"""
from core.application import Application
from ui.console_menu import ConsoleMenu

def main():
    app = Application()
    try:
        app.startup()

#        app.run()
        menu = ConsoleMenu(app)
        menu.run()

    finally:

        app.shutdown()

if __name__ == "__main__":
    main()