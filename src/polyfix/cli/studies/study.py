from cyclopts import App
from utils4plans.logs import logset

app = App()


@app.command()
def welcome():
    return "Welcome to polymap"


def main():
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()
