import tempfile
from pathlib import Path

from fastapi import FastAPI
from starlette.responses import FileResponse, Response
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse, Response

from domain import Pokemon
from internal import Database
from pypika import PostgreSQLQuery, Field
from dict2xml import dict2xml

db: Database
static: str

api = FastAPI(title="Pokedex", description="Pokedex endpoints")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_image(path: str) -> FileResponse | Response:
    if Path(path).exists():
        return FileResponse(path=path)
    return Response(status_code=404, content="File not found")


@api.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@api.get(
    path="/static/images/{name}/artwork.png",
    name="Cover",
    description="Pokemon cover image",
    include_in_schema=True,
    responses={200: {"description": "success"}, 404: {"description": "Not found"}},
)
async def cover(name: str):
    path = "{static}/images/{name}/artwork.png".format(static=static, name=name)
    return get_image(path)


@api.get(
    path="/static/images/{name}/animated/back.gif",
    name="Animated Back",
    description="Pokemon animated front image",
    include_in_schema=True,
    responses={200: {"description": "success"}, 404: {"description": "Not found"}},
)
async def animated_back(name: str):
    path = "{static}/images/{name}/animated/back.gif".format(static=static, name=name)
    return get_image(path)


@api.get(
    path="/static/images/{name}/animated/front.gif",
    name="Animated Front",
    description="Pokemon animated front image",
    include_in_schema=True,
    responses={200: {"description": "success"}, 404: {"description": "Not found"}},
)
async def animated_front(name: str):
    path = "{static}/images/{name}/animated/front.gif".format(static=static, name=name)
    return get_image(path)


@api.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(path="./resources/favicon.png")


@api.get(
    path="/pokemons",
    name="Pokemons",
    summary="Get all pokemons",
)
async def pokemons(offset: int | None = None, limit: int | None = None) -> list[Pokemon]:
    query = PostgreSQLQuery()
    query = query.from_("pokemon").select(
        "id",
        "external_id",
        "name",
        "weight",
        "height",
        "types",
        "hp",
        "speed",
        "attack",
        "defense",
        "images"
    ).offset(offset).limit(limit).orderby("name")

    result = []

    for entry in db.fetchall(query=query.get_sql()):
        result.append(Pokemon(data=entry))

    return result


@api.get(
    path="/pokemons/{name}",
    name="Pokemon",
    summary="Get a pokemon by name",
    response_model=Pokemon,
    responses={200: {"model": Pokemon}, 404: {"description": "Not found"}},
)
async def find_pokemon_by_name(name: str) -> Pokemon | Response:
    query = PostgreSQLQuery()
    query = query.from_("pokemon").select(
        "id",
        "external_id",
        "name",
        "weight",
        "height",
        "types",
        "hp",
        "speed",
        "attack",
        "defense",
        "images"
    ).where(Field("name") == name)

    result = db.fetchone(query=query.get_sql())
    if result is not None:
        return Pokemon(data=result)

    return Response(status_code=404, content="Pokemon not found")


@api.get(
    path="/pokemons/{name}/export",
    name="Pokemon",
    summary="Export a pokemon into a XML file",
    responses={200: {"description": "XML File"}, 404: {"description": "Not found"}},
)
async def export_pokemon_by_name(name: str):
    query = PostgreSQLQuery()
    query = query.from_("pokemon").select(
        "id",
        "external_id",
        "name",
        "weight",
        "height",
        "types",
        "hp",
        "speed",
        "attack",
        "defense",
        "images"
    ).where(Field("name") == name)

    result = db.fetchone(query=query.get_sql())
    if result is not None:
        file = tempfile.NamedTemporaryFile(mode="w+", suffix=".xml", delete=False)
        file.write(dict2xml(Pokemon(data=result).to_dict(), wrap='root'))
        file.seek(0)

        return FileResponse(path=file.name)

    return Response(status_code=404, content="Pokemon not found")


def serve(host: str, port: int, database: Database, static_folder: str):
    global static
    global db
    global api

    static = static_folder
    db = database

    run(api, host=host, port=port)
