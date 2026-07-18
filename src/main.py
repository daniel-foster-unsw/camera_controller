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

        mode = app.configuration.get(
            "communication",
            "mode"
        )

        if mode == "menu":

            menu = ConsoleMenu(app)
            menu.run()

        else:

            app.run()
    except KeyboardInterrupt:
        print("\nShutdown requested by user.")    

    except Exception as ex:
        print(f"\nFatal error: {ex}")
        raise

    finally:
        print("Shutting down...")
        app.shutdown()

if __name__ == "__main__":
    main()