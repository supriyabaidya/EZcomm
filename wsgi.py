from flask import Flask
from server import main

application = Flask(__name__)


@application.route("/")
def hello():
    main()
    return "server closed"


if __name__ == "__main__":
    application.run()
