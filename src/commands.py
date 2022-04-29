import click
from src.db.access import UserAccess
from src.db.models import User

user_access = UserAccess()


def init_commands(app):
    """ Создание супер пользователя """
    @app.cli.command("create_superuser")
    @click.argument("username")
    @click.argument("password")
    def create_user(username: str, password: str):
        User.validate_username(username)
        user_access.create(**{'username': username, 'password': password, 'is_superuser': True})
        click.echo('User created')
