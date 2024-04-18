import os
from dotenv import load_dotenv
from flask import Flask
from board import pages, posts, store

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    store.init_app(app)

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)

    print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
    print(f"Using Database : {app.config.get("DATABASE")}")
    return app





#
# @app.route('/')
# def home():  # put application's code here
#     return 'Hello fast World!'
#
#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8000, debug=True)
