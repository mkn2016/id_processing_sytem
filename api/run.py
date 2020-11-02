from os import urandom, environ
from typing import NoReturn

from flask import Flask, g, abort
from rethinkdb import r
from rethinkdb.errors import RqlDriverError

from api.extensions import mail
from api.views import auth as auth_blueprint


class APIServer(Flask):
    def __init__(self, environment="development"):
        super().__init__(__name__)
        self.environment = environment

    def load_config(self) -> NoReturn:
        self.config.from_object("config.Config")

    def handle_requests(self) -> NoReturn:
        @self.before_request
        def before_request() -> NoReturn:
            try:
                g.con = r.connect(host="localhost", port=28015, db="id_card_processing_system")
            except RqlDriverError:
                abort(503, "No database connection could be established")

        @self.teardown_request
        def teardown_request(exception) -> NoReturn:
            try:
                g.con.close()
            except AttributeError:
                pass

        return before_request, teardown_request

    def init_mail(self) -> NoReturn:
        mail.init_app(self)

    def register_blue_prints(self) -> NoReturn:
        self.register_blueprint(auth_blueprint)

    def start(self, host: str = None, port: int = None) -> NoReturn:
        if self.environment == "development":
            if host and port:
                self.run(host=host, port=port, debug=True)
            elif not (host and port):
                self.run(host="0.0.0.0", port=5000, debug=True)
            elif host and not port:
                self.run(host=host, port=5000, debug=True)
            elif not host and port:
                self.run(host="0.0.0.0", port=port, debug=True)
        elif self.environment == "staging" or self.environment == "production":
            self.run(host=host, port=port, debug=False)

    def main(self):
        self.init_mail()
        self.load_config()
        self.register_blue_prints()
        self.handle_requests()
        self.start()


if __name__ == "__main__":
    app = APIServer()
    app.main()
