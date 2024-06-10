# This is a sample Python script.
from shutil import rmtree

import typer
from dotenv import dotenv_values
from pgMigrationMgr import MigrationMgr
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from simplejsondb import DatabaseFolder

from domain import Pokemon
from internal import get_env_variable, database
from internal.constants import POKEAPI
from internal.scrap import get_all_pokemons_links, get_pokemon
from internal.api import serve

cli = typer.Typer(no_args_is_help=True, add_completion=False)
envs = {}


@cli.command("collect", short_help="Scrap all pokemons and download images")
def collect(limit: bool = False, limit_size: int = 5, overwrite: bool = False):
    folder = get_env_variable(envs, "COLLECT_FOLDER")
    static_folder = get_env_variable(envs, "STATIC_FOLDER")

    rmtree(static_folder, ignore_errors=True)

    localdb = DatabaseFolder(folder)

    continue_collecting = True
    if localdb['pokemons_ref'] is not None or localdb['pokemons'] is not None:
        def is_valid_option(option):
            return option == 'y' or option == 'n'

        validator = Validator.from_callable(
            is_valid_option,
            error_message="Invalid option",
            move_cursor_to_end=True,
        )

        answer = prompt(
            message="You've already collected data, would you like to overwrite it? (y/n) ",
            default="y",
            accept_default=overwrite,
            validator=validator,
        )

        if answer == "n":
            continue_collecting = False

    if continue_collecting:
        localdb['pokemons'] = []
        localdb['pokemons_ref'] = get_all_pokemons_links(POKEAPI)
        for ref in localdb['pokemons_ref'][:limit_size if limit else None]:
            pokemon = get_pokemon(ref['name'], ref['url'], static_folder)
            if pokemon is not None:
                localdb['pokemons'].append(pokemon.to_dict())

    print("\n\nProcess finished")
    exit(0)


@cli.command("migrate", short_help="Migrate all pokemon data to a database")
def migrate():
    folder = get_env_variable(envs, "COLLECT_FOLDER")

    migrations_folder = get_env_variable(envs, "MIGRATIONS_FOLDER")

    db = database(envs=envs)
    db.open()

    migration = MigrationMgr(conn=db.conn, migrations_path=migrations_folder, verbose=True)
    migration.destroy()
    migration.create()

    localdb = DatabaseFolder(folder)

    for data in localdb['pokemons']:
        pokemon = Pokemon(data=data)
        db.execute(pokemon.get_insert_statement())
        print("\n\tInserting {}".format(pokemon.name), end="")

    print("\n\nProcess finished")
    exit(0)


@cli.command("start", short_help="Start server")
def start(host: str = "localhost", port: int = 3000):
    static_folder = get_env_variable(envs, "STATIC_FOLDER")
    db = database(envs=envs)
    db.open()
    serve(host=host, port=port, database=db, static_folder=static_folder)


if __name__ == '__main__':
    print("Running")
    envs = dotenv_values(".env")
    cli()
