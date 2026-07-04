"""
main.py

Program entry point.
"""
from core.application import Application

def main():
    app = Application()
    try:
        app.startup()

        app.run()

    finally:

        app.shutdown()

if __name__ == "__main__":
    main()