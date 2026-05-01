"""WSGI entrypoint for production API serving."""

from app import app


def create_app():
    return app
